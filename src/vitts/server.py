"""API server tương thích OpenAI (`POST /v1/audio/speech`).

Chạy:
    vitts-server --port 8000
Gọi thử:
    curl localhost:8000/v1/audio/speech -H 'Content-Type: application/json' \
        -d '{"input": "Xin chào Việt Nam", "response_format": "wav"}' -o out.wav

Hoặc dùng thư viện `openai`:
    client = OpenAI(base_url="http://localhost:8000/v1", api_key="none")
    client.audio.speech.create(model="vitts", voice="default", input="Xin chào").write_to_file("out.wav")
"""

import argparse
import io
import os
from typing import Literal, Protocol

import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, Field

from vitts.text import normalize_text

MEDIA_TYPES = {"wav": "audio/wav", "flac": "audio/flac", "pcm": "audio/pcm"}


class Synthesizer(Protocol):
    model_name: str
    sample_rate: int

    def synthesize(self, text: str, speed: float = 1.0, speaker: str | None = None): ...


class SpeechRequest(BaseModel):
    input: str = Field(..., min_length=1, max_length=5000)
    model: str = "vitts"
    voice: str | None = None
    response_format: Literal["wav", "flac", "pcm"] = "wav"
    speed: float = Field(1.0, ge=0.25, le=4.0)


class NormalizeRequest(BaseModel):
    input: str = Field(..., max_length=5000)


def encode(samples: np.ndarray, sample_rate: int, fmt: str) -> bytes:
    if fmt == "pcm":  # 16-bit little-endian mono, giống OpenAI
        return (np.clip(samples, -1, 1) * 32767).astype("<i2").tobytes()
    import soundfile as sf

    buf = io.BytesIO()
    sf.write(buf, samples, sample_rate, format=fmt.upper(), subtype="PCM_16")
    return buf.getvalue()


def create_app(tts: Synthesizer) -> FastAPI:
    app = FastAPI(title="Vietnamese TTS", version="0.1.0")

    @app.get("/health")
    def health():
        return {"status": "ok", "model": tts.model_name, "sample_rate": tts.sample_rate}

    @app.get("/v1/models")
    def models():
        return {"object": "list", "data": [{"id": "vitts", "object": "model", "owned_by": tts.model_name}]}

    @app.post("/v1/normalize")
    def normalize(req: NormalizeRequest):
        return {"text": normalize_text(req.input)}

    @app.post("/v1/audio/speech")
    def speech(req: SpeechRequest):
        voice = None if req.voice in (None, "", "default", "alloy") else req.voice
        try:
            audio = tts.synthesize(req.input, speed=req.speed, speaker=voice)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e
        return Response(
            content=encode(audio.samples, audio.sample_rate, req.response_format),
            media_type=MEDIA_TYPES[req.response_format],
        )

    return app


def main():
    parser = argparse.ArgumentParser(description="Vietnamese TTS server (OpenAI-compatible)")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--model-name", default=os.getenv("VITTS_MODEL_NAME"))
    parser.add_argument("--model-path", default=os.getenv("VITTS_MODEL_PATH"))
    parser.add_argument("--config-path", default=os.getenv("VITTS_CONFIG_PATH"))
    parser.add_argument("--gpu", action="store_true")
    args = parser.parse_args()

    import uvicorn

    from vitts.synthesizer import DEFAULT_MODEL, VietnameseTTS

    tts = VietnameseTTS(
        model_name=args.model_name or DEFAULT_MODEL,
        model_path=args.model_path,
        config_path=args.config_path,
        gpu=args.gpu,
    )
    uvicorn.run(create_app(tts), host=args.host, port=args.port)


if __name__ == "__main__":
    main()
