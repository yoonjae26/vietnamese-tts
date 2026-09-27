"""Chấm audio của các model: độ rõ (ASR nghe lại, WER/CER), lỗi không dừng, độ tự nhiên (UTMOS)
và độ giống giọng mẫu (SIM, chỉ với model clone giọng). Xem `quality.py`.

    CUDA_VISIBLE_DEVICES=0 python benchmark/tts/evaluate.py            # mọi model đã sinh audio
    CUDA_VISIBLE_DEVICES=0 python benchmark/tts/evaluate.py mms vixtts

Ghi `outputs/tts/<engine>/{asr,quality}.json` (cache) và bảng tổng hợp `results/tts.md`, `results/tts.json`.
"""

import argparse
import json
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

import jiwer
import numpy as np
import soundfile as sf
import torch
from quality import CLONING, Scorers, load_16k
from synthesize import pick_device  # dùng chung chốt chặn GPU

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "src"))

from vitts.bench.metrics import canonicalize  # noqa: E402

ASR_MODEL = "vinai/PhoWhisper-large"
RUNAWAY_FACTOR = 3


def load_asr(device: str):
    from transformers import pipeline

    return pipeline(
        "automatic-speech-recognition",
        model=ASR_MODEL,
        device=device,
        torch_dtype=torch.float16 if device.startswith("cuda") else torch.float32,
    )


def transcribe(asr, wav_path: Path) -> str:
    audio, sr = sf.read(wav_path, dtype="float32")
    if audio.ndim > 1:
        audio = audio.mean(axis=1)
    if sr != 16000:
        import librosa

        audio = librosa.resample(audio, orig_sr=sr, target_sr=16000)
    audio = np.ascontiguousarray(audio)
    return asr({"raw": audio, "sampling_rate": 16000}, generate_kwargs={"language": "vi", "task": "transcribe"})["text"]


def score_quality(scorers: Scorers, run_dir: Path, meta: dict) -> dict:
    cache_file = run_dir / "quality.json"
    cache = json.loads(cache_file.read_text(encoding="utf-8")) if cache_file.exists() else {}
    for s in meta["sentences"]:
        if s["id"] not in cache:
            wav = load_16k(run_dir / f"{s['id']}.wav")
            cache[s["id"]] = {"utmos": scorers.mos(wav), "sim": scorers.similarity(wav)}
    cache_file.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")
    return {
        "utmos": float(np.mean([cache[s["id"]]["utmos"] for s in meta["sentences"]])),
        "sim": float(np.mean([cache[s["id"]]["sim"] for s in meta["sentences"]])),
        "clones_voice": meta["engine"] in CLONING,
    }


def evaluate_engine(asr, scorers: Scorers, run_dir: Path) -> dict:
    meta = json.loads((run_dir / "meta.json").read_text(encoding="utf-8"))
    cache_file = run_dir / "asr.json"
    cache = json.loads(cache_file.read_text(encoding="utf-8")) if cache_file.exists() else {}

    rows = []
    for s in meta["sentences"]:
        if s["id"] not in cache:
            cache[s["id"]] = transcribe(asr, run_dir / f"{s['id']}.wav")
        ref, hyp = canonicalize(s["text"]), canonicalize(cache[s["id"]])
        rows.append(
            {
                "id": s["id"],
                "category": s["category"],
                "ref": ref,
                "hyp": hyp,
                "wer": jiwer.wer(ref, hyp),
                "cer": jiwer.cer(ref, hyp),
                "ref_words": len(ref.split()),
            }
        )
    cache_file.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")

    def corpus(rs):  # WER/CER theo toàn bộ tập (không phải trung bình từng câu)
        refs, hyps = [r["ref"] for r in rs], [r["hyp"] for r in rs]
        return {"wer": jiwer.wer(refs, hyps), "cer": jiwer.cer(refs, hyps), "n": len(rs)}

    by_cat = defaultdict(list)
    for r in rows:
        by_cat[r["category"]].append(r)

    # Lỗi "không dừng": ASR bỏ qua khoảng lặng thừa nên WER không thấy, nhưng người dùng phải chờ.
    # Một câu bị coi là bất thường khi số giây/từ > 3 lần trung vị của chính model đó.
    sec_per_word = [s["audio_seconds"] / max(len(s["text"].split()), 1) for s in meta["sentences"]]
    median = float(np.median(sec_per_word))
    runaway = [s["id"] for s, x in zip(meta["sentences"], sec_per_word, strict=True) if x > RUNAWAY_FACTOR * median]
    return {
        "engine": meta["engine"],
        "name": meta["name"],
        "repo": meta["repo"],
        "license": meta["license"],
        "device": meta["device"],
        "rtf": meta["rtf"],
        "peak_vram_gb": meta["peak_vram_gb"],
        "sample_rate": meta["sample_rate"],
        "overall": corpus(rows),
        "by_category": {c: corpus(rs) for c, rs in by_cat.items()},
        "runaway": runaway,
        **score_quality(scorers, run_dir, meta),
        "rows": rows,
    }


def to_markdown(results: list[dict], reference: dict) -> str:
    cats = list(results[0]["by_category"])
    lines = [
        f"# Benchmark TTS tiếng Việt ({date.today().isoformat()})",
        "",
        f"ASR chấm điểm: `{ASR_MODEL}`. {results[0]['overall']['n']} câu. WER/CER càng thấp càng rõ. "
        "RTF = thời gian sinh / độ dài audio (càng thấp càng nhanh). "
        f"**Không dừng** = số câu có giây/từ > {RUNAWAY_FACTOR}× trung vị của model (sinh thừa khoảng lặng "
        "hoặc âm rác; WER không phát hiện được). "
        "**UTMOS** = điểm tự nhiên dự đoán 1–5 (model huấn luyện trên tiếng Anh, chỉ so sánh tương đối). "
        "**SIM** = độ giống giọng mẫu (cosine ECAPA-TDNN). MMS và Piper không clone giọng (giọng cố định của "
        "người khác), SIM của chúng là mốc cho hai người nói khác nhau. "
        f"Chính giọng mẫu: UTMOS {reference['utmos']:.2f}.",
        "",
        "| Model | WER | CER | "
        + " | ".join(f"WER {c}" for c in cats)
        + " | Không dừng | UTMOS | SIM | RTF | VRAM | Hz | Giấy phép |",
        "|---|---:|---:|" + "---:|" * len(cats) + "---:|---:|---:|---:|---:|---:|---|",
    ]
    for r in sorted(results, key=lambda r: r["overall"]["wer"]):
        o = r["overall"]
        vram = f"{r['peak_vram_gb']:.1f} GB" if r["peak_vram_gb"] is not None else "– (CPU)"
        sim = f"{r['sim']:.3f}" if r["clones_voice"] else f"({r['sim']:.3f})"
        lines.append(
            f"| [{r['name']}](https://huggingface.co/{r['repo']}) | **{o['wer']:.1%}** | {o['cer']:.1%} | "
            + " | ".join(f"{r['by_category'][c]['wer']:.1%}" for c in cats)
            + f" | {len(r['runaway'])}/{o['n']} | {r['utmos']:.2f} | {sim} | {r['rtf']:.3f} | {vram}"
            + f" | {r['sample_rate']} | {r['license']} |"
        )
    lines += ["", f"GPU: {next(r['device'] for r in results if r['peak_vram_gb'] is not None)}.", ""]
    for r in results:
        if r["runaway"]:
            lines.append(f"- {r['name']}: câu không dừng: {', '.join(r['runaway'])}")
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("engines", nargs="*", help="mặc định: mọi thư mục trong outputs/tts")
    parser.add_argument("--outputs", default=str(ROOT / "outputs" / "tts"))
    args = parser.parse_args()

    device = pick_device(cpu=False)
    out_root = Path(args.outputs)
    names = args.engines or sorted(p.name for p in out_root.iterdir() if (p / "meta.json").exists())

    sys.path.insert(0, str(HERE))
    from engines.common import reference

    ref_wav = reference()[0]
    asr = load_asr(device)
    scorers = Scorers(device, ref_wav)
    ref_scores = {"utmos": scorers.mos(load_16k(ref_wav))}
    results = [evaluate_engine(asr, scorers, out_root / n) for n in names]
    for r in results:
        print(
            f"{r['engine']:12s} WER={r['overall']['wer']:.1%} UTMOS={r['utmos']:.2f} SIM={r['sim']} RTF={r['rtf']:.3f}"
        )

    res_dir = ROOT / "results"
    res_dir.mkdir(exist_ok=True)
    md = to_markdown(results, ref_scores)
    (res_dir / "tts.md").write_text(md, encoding="utf-8")
    payload = {"reference": ref_scores, "engines": results}
    (res_dir / "tts.json").write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(md)


if __name__ == "__main__":
    main()
