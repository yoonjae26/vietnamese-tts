"""API TTS tiếng Việt tương thích OpenAI (`POST /v1/audio/speech`), chọn model bằng tham số `model`.

Mỗi model chạy trong một worker riêng (`benchmark/tts/worker.py`, trong môi trường conda của model đó),
vì các model cần những phiên bản thư viện xung đột nhau. Gateway này nhận yêu cầu, chuẩn hóa văn bản
tiếng Việt (đọc số, ngày giờ, viết tắt…), tách câu, gửi tới worker rồi ghép audio.

Chạy (xem `benchmark/tts/serve_all.sh` để bật cả worker):
    vitts-server --worker f5=http://127.0.0.1:9103 --worker vieneu=http://127.0.0.1:9104
    # hoặc VITTS_WORKERS="f5=http://127.0.0.1:9103,vieneu=http://127.0.0.1:9104" vitts-server

Gọi thử:
    curl localhost:8000/v1/audio/speech -H 'Content-Type: application/json' \
        -d '{"model": "vieneu", "input": "Giá 100k, giao lúc 14h30."}' -o out.wav

    client = OpenAI(base_url="http://localhost:8000/v1", api_key="none")
    client.audio.speech.create(model="f5", voice="default", input="Xin chào").write_to_file("out.wav")

`voice` được chấp nhận để tương thích OpenAI nhưng hiện mọi model dùng giọng mặc định của nó
(model clone giọng dùng giọng mẫu của benchmark).
"""

import argparse
import io
import json
import logging
import os
import urllib.error
import urllib.parse
import urllib.request
import wave
from dataclasses import dataclass
from typing import Literal, Protocol

import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, Field

from vitts.text import normalize_text, split_sentences

log = logging.getLogger("vitts.server")
MEDIA_TYPES = {"wav": "audio/wav", "flac": "audio/flac", "pcm": "audio/pcm"}
PAUSE_SECONDS = 0.15


@dataclass
class Audio:
    samples: np.ndarray  # float32 mono [-1, 1]
    sample_rate: int


class Backend(Protocol):
    info: dict  # engine, name, license, sample_rate, ...

    def synthesize(self, text: str, seed: int) -> Audio: ...


class BackendError(RuntimeError):
    pass


def decode_wav(data: bytes) -> Audio:
    with wave.open(io.BytesIO(data)) as w:
        pcm = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2")
        return Audio(pcm.astype(np.float32) / 32767.0, w.getframerate())


class RemoteBackend:
    """Worker HTTP của một model (benchmark/tts/worker.py)."""

    def __init__(self, url: str, timeout: float = 300):
        self.url = url.rstrip("/")
        self.timeout = timeout
        with urllib.request.urlopen(f"{self.url}/health", timeout=10) as r:
            self.info = json.load(r)

    def synthesize(self, text: str, seed: int) -> Audio:
        req = urllib.request.Request(
            f"{self.url}/synth",
            data=json.dumps({"text": text, "seed": seed}).encode(),
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                return decode_wav(r.read())
        except (urllib.error.URLError, TimeoutError) as e:
            raise BackendError(f"worker {self.url} lỗi: {e}") from e


class LocalBackend:
    """Chạy MMS ngay trong tiến trình gateway (không cần worker), dùng `vitts.synthesizer`."""

    def __init__(self):
        from vitts.synthesizer import DEFAULT_MODEL, VietnameseTTS

        self.tts = VietnameseTTS(DEFAULT_MODEL)
        self.info = {"engine": "mms", "name": "MMS-TTS (Meta)", "license": "CC-BY-NC-4.0",
                     "sample_rate": self.tts.sample_rate}  # fmt: skip

    def synthesize(self, text: str, seed: int) -> Audio:  # noqa: ARG002
        wav = self.tts._tts.tts(text, split_sentences=False)
        return Audio(np.asarray(wav, dtype=np.float32), self.tts.sample_rate)


class SpeechRequest(BaseModel):
    input: str = Field(..., min_length=1, max_length=5000)
    model: str | None = None
    voice: str | None = None
    response_format: Literal["wav", "flac", "pcm"] = "wav"
    speed: float = Field(1.0, ge=0.25, le=4.0)
    normalize: bool = True
    seed: int = 1234


class NormalizeRequest(BaseModel):
    input: str = Field(..., max_length=5000)


def encode(samples: np.ndarray, sample_rate: int, fmt: str) -> bytes:
    if fmt == "pcm":  # 16-bit little-endian mono, giống OpenAI
        return (np.clip(samples, -1, 1) * 32767).astype("<i2").tobytes()
    import soundfile as sf

    buf = io.BytesIO()
    sf.write(buf, samples, sample_rate, format=fmt.upper(), subtype="PCM_16")
    return buf.getvalue()


def create_app(backends: dict[str, Backend], default_model: str | None = None) -> FastAPI:
    if not backends:
        raise ValueError("Cần ít nhất một model")
    default_model = default_model or next(iter(backends))
    app = FastAPI(title="Vietnamese TTS", version="0.2.0")

    def pick(model: str | None) -> tuple[str, Backend]:
        name = model if model in backends else None
        if model in (None, "", "tts-1", "tts-1-hd", "vitts"):  # tên model mặc định của OpenAI
            name = default_model
        if name is None:
            raise HTTPException(404, f"Không có model '{model}'. Có: {', '.join(backends)}")
        return name, backends[name]

    @app.get("/health")
    def health():
        return {"status": "ok", "default_model": default_model, "models": list(backends)}

    @app.get("/v1/models")
    def models():
        return {
            "object": "list",
            "data": [
                {"id": name, "object": "model", "owned_by": b.info.get("name", name), "license": b.info.get("license")}
                for name, b in backends.items()
            ],
        }

    @app.post("/v1/normalize")
    def normalize(req: NormalizeRequest):
        return {"text": normalize_text(req.input)}

    @app.post("/v1/audio/speech")
    def speech(req: SpeechRequest):
        name, backend = pick(req.model)
        text = normalize_text(req.input) if req.normalize else req.input.strip()
        chunks = split_sentences(text, max_chars=200)
        if not chunks:
            raise HTTPException(400, "Văn bản rỗng sau khi chuẩn hóa")

        pieces, sample_rate = [], None
        for chunk in chunks:
            try:
                audio = backend.synthesize(chunk, seed=req.seed)
            except BackendError as e:
                raise HTTPException(502, str(e)) from e
            sample_rate = sample_rate or audio.sample_rate
            pieces += [audio.samples, np.zeros(int(sample_rate * PAUSE_SECONDS), dtype=np.float32)]
        samples = np.concatenate(pieces[:-1])

        if req.speed != 1.0:
            try:
                import librosa
            except ImportError as e:
                raise HTTPException(400, "speed khác 1.0 cần cài librosa") from e
            samples = librosa.effects.time_stretch(samples, rate=req.speed)

        return Response(
            content=encode(samples, sample_rate, req.response_format),
            media_type=MEDIA_TYPES[req.response_format],
            headers={"X-Model": name, "X-Normalized-Text": urllib.parse.quote(text[:500])},
        )

    return app


def parse_workers(items: list[str]) -> dict[str, str]:
    out = {}
    for item in items:
        for part in filter(None, (p.strip() for p in item.split(","))):
            name, _, url = part.partition("=")
            if not url:
                raise SystemExit(f"--worker cần dạng tên=url, nhận được '{part}'")
            out[name] = url
    return out


def main():
    parser = argparse.ArgumentParser(description="Vietnamese TTS gateway (OpenAI-compatible)")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--worker", action="append", default=[], help="tên=url, lặp lại được")
    parser.add_argument("--default-model", default=os.getenv("VITTS_DEFAULT_MODEL"))
    parser.add_argument("--local", action="store_true", help="chạy MMS trong tiến trình, không cần worker")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)

    workers = parse_workers(args.worker + ([os.environ["VITTS_WORKERS"]] if os.getenv("VITTS_WORKERS") else []))
    backends: dict[str, Backend] = {}
    for name, url in workers.items():
        try:
            backends[name] = RemoteBackend(url)
            log.info("model %s -> %s (%s)", name, url, backends[name].info.get("name"))
        except OSError as e:
            log.warning("bỏ qua model %s: không kết nối được %s (%s)", name, url, e)
    if args.local:
        backends["mms"] = LocalBackend()
    if not backends:
        raise SystemExit("Không có model nào: dùng --worker tên=url (xem benchmark/tts/serve_all.sh) hoặc --local")

    import uvicorn

    uvicorn.run(create_app(backends, args.default_model), host=args.host, port=args.port)


if __name__ == "__main__":
    main()
