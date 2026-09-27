"""Sinh audio cho một model trên toàn bộ `sentences.jsonl`, đo tốc độ và VRAM.

    CUDA_VISIBLE_DEVICES=0 python benchmark/tts/synthesize.py --engine mms

Ghi ra:
    outputs/tts/<engine>/<id>.wav
    outputs/tts/<engine>/meta.json   # RTF, VRAM, thời gian từng câu
"""

import argparse
import importlib
import json
import os
import platform
import sys
import time
from pathlib import Path

import soundfile as sf
import torch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

from engines import ENGINES  # noqa: E402

# Máy dùng chung: chỉ được phép chạy trên GPU 0.
ALLOWED_GPU = "0"


def pick_device(cpu: bool) -> str:
    if cpu:
        return "cpu"
    visible = os.environ.get("CUDA_VISIBLE_DEVICES")
    if visible != ALLOWED_GPU:
        sys.exit(f"Từ chối chạy: cần đặt CUDA_VISIBLE_DEVICES={ALLOWED_GPU} (hiện tại: {visible!r}).")
    if not torch.cuda.is_available():
        sys.exit("Không thấy GPU.")
    return "cuda:0"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--engine", required=True, choices=list(ENGINES))
    parser.add_argument("--cpu", action="store_true", help="chạy trên CPU để đo RTF CPU")
    parser.add_argument("--limit", type=int, default=None, help="chỉ chạy N câu đầu (thử nhanh)")
    parser.add_argument("--seed", type=int, default=1234)
    parser.add_argument("--out", default=str(ROOT / "outputs" / "tts"))
    args = parser.parse_args()

    device = pick_device(args.cpu)
    sentences = [json.loads(x) for x in (HERE / "sentences.jsonl").read_text(encoding="utf-8").splitlines() if x]
    sentences = sentences[: args.limit]

    module, _env = ENGINES[args.engine]
    Engine = importlib.import_module(module).Engine

    t0 = time.perf_counter()
    engine = Engine(device)
    load_seconds = time.perf_counter() - t0
    engine.synth("xin chào.", seed=args.seed)  # warm-up
    if device.startswith("cuda"):
        torch.cuda.synchronize()
        torch.cuda.reset_peak_memory_stats()

    run_dir = Path(args.out) / (args.engine + ("-cpu" if args.cpu else ""))
    run_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for i, s in enumerate(sentences, 1):
        t = time.perf_counter()
        wav = engine.synth(s["text"], seed=args.seed)
        if device.startswith("cuda"):
            torch.cuda.synchronize()
        seconds = time.perf_counter() - t
        duration = len(wav) / engine.sample_rate
        sf.write(run_dir / f"{s['id']}.wav", wav, engine.sample_rate, subtype="PCM_16")
        rows.append({**s, "synth_seconds": seconds, "audio_seconds": duration, "rtf": seconds / max(duration, 1e-6)})
        print(f"[{i}/{len(sentences)}] {s['id']}: {duration:.1f}s audio / {seconds:.2f}s")

    meta = {
        "engine": args.engine,
        "name": engine.name,
        "repo": engine.repo,
        "license": engine.license,
        "device": torch.cuda.get_device_name(0) if device.startswith("cuda") else platform.processor() or "cpu",
        "sample_rate": engine.sample_rate,
        "load_seconds": load_seconds,
        "peak_vram_gb": torch.cuda.max_memory_allocated() / 1e9 if device.startswith("cuda") else None,
        "total_synth_seconds": sum(r["synth_seconds"] for r in rows),
        "total_audio_seconds": sum(r["audio_seconds"] for r in rows),
        "seed": args.seed,
        "sentences": rows,
    }
    meta["rtf"] = meta["total_synth_seconds"] / meta["total_audio_seconds"]
    (run_dir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"RTF={meta['rtf']:.3f}  VRAM={meta['peak_vram_gb']}  -> {run_dir}")


if __name__ == "__main__":
    main()
