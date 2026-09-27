"""Worker HTTP cho một model TTS, chạy trong môi trường conda của model đó.

Chỉ dùng thư viện chuẩn (không cần cài thêm gì vào môi trường của model):

    CUDA_VISIBLE_DEVICES=0 python benchmark/tts/worker.py --engine f5 --port 9103

    GET  /health  -> {"engine", "name", "license", "sample_rate", "repo"}
    POST /synth   {"text": "...", "seed": 1234} -> audio/wav (PCM 16-bit mono)

Gateway `vitts-server` (src/vitts/server.py) gom các worker lại thành một API tương thích OpenAI.
"""

import argparse
import io
import json
import sys
import threading
import wave
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from engines import ENGINES  # noqa: E402
from synthesize import pick_device  # noqa: E402  (chốt chặn: chỉ GPU 0)

MAX_CHARS = 2000


def to_wav(samples: np.ndarray, sample_rate: int) -> bytes:
    pcm = (np.clip(samples, -1.0, 1.0) * 32767).astype("<i2").tobytes()
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        w.writeframes(pcm)
    return buf.getvalue()


def make_handler(engine, engine_id: str):
    lock = threading.Lock()  # model không an toàn khi gọi song song
    info = {
        "engine": engine_id,
        "name": engine.name,
        "license": engine.license,
        "repo": engine.repo,
        "sample_rate": engine.sample_rate,
    }

    class Handler(BaseHTTPRequestHandler):
        def _json(self, code: int, obj: dict):
            body = json.dumps(obj, ensure_ascii=False).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):  # noqa: N802
            if self.path == "/health":
                self._json(200, info)
            else:
                self._json(404, {"error": "not found"})

        def do_POST(self):  # noqa: N802
            if self.path != "/synth":
                return self._json(404, {"error": "not found"})
            try:
                req = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
                text = str(req.get("text", "")).strip()
                seed = int(req.get("seed", 1234))
            except (ValueError, json.JSONDecodeError):
                return self._json(400, {"error": "body phải là JSON {text, seed}"})
            if not text or len(text) > MAX_CHARS:
                return self._json(400, {"error": f"text phải có từ 1 đến {MAX_CHARS} ký tự"})
            with lock:
                wav = engine.synth(text, seed=seed)
            body = to_wav(wav, engine.sample_rate)
            self.send_response(200)
            self.send_header("Content-Type", "audio/wav")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, fmt, *args):
            sys.stderr.write(f"[{engine_id}] {fmt % args}\n")

    return Handler


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--engine", required=True, choices=list(ENGINES))
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--cpu", action="store_true")
    args = parser.parse_args()

    import importlib

    device = pick_device(args.cpu)
    engine = importlib.import_module(ENGINES[args.engine][0]).Engine(device)
    engine.synth("xin chào.", seed=0)  # warm-up
    server = ThreadingHTTPServer((args.host, args.port), make_handler(engine, args.engine))
    print(f"READY {args.engine} http://{args.host}:{args.port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
