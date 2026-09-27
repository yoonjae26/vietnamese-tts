"""Đánh giá phiên âm từ nước ngoài trên bộ test (từ chưa gặp khi huấn luyện).

    CUDA_VISIBLE_DEVICES=0 python training/translit/evaluate.py

Chỉ số (so với đáp án gần nhất khi một từ có nhiều cách đọc đúng):
- Đúng cả từ: output trùng khớp một đáp án
- SER: tỉ lệ lỗi âm tiết (edit distance trên âm tiết / số âm tiết đáp án)
- CER: tỉ lệ lỗi ký tự
"""

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).parent))

from prepare_data import clean_target  # noqa: E402
from train import read  # noqa: E402

from vitts.bench.metrics import edit_distance  # noqa: E402


def score(pred: str, refs: list[str]) -> dict:
    pred = clean_target(pred)
    best = None
    for ref in refs:
        syl = edit_distance(pred.split(), ref.split()) / max(len(ref.split()), 1)
        ch = edit_distance(list(pred.replace(" ", "")), list(ref.replace(" ", ""))) / max(len(ref.replace(" ", "")), 1)
        cand = {"exact": pred == ref, "ser": syl, "cer": ch}
        if best is None or (cand["exact"], -cand["ser"], -cand["cer"]) > (best["exact"], -best["ser"], -best["cer"]):
            best = cand
    return best


def systems():
    from vitts.translit import Transliterator

    yield "Giữ nguyên chữ tiếng Anh", lambda w: w

    from vietnormalizer.transliterator import transliterate_word

    yield "vietnormalizer (quy tắc, không tra từ điển)", transliterate_word

    from soe_vinorm import SoeNormalizer

    soe = SoeNormalizer()
    yield "soe-vinorm", lambda w: soe.normalize(w)

    greedy = Transliterator.from_pretrained(device="cuda:0", beam=1)
    yield "vitts translit (greedy)", greedy
    beam = Transliterator.from_pretrained(device="cuda:0", beam=5)
    yield "vitts translit (beam 5)", beam


def main():
    import os

    if os.environ.get("CUDA_VISIBLE_DEVICES") != "0":
        sys.exit("Cần CUDA_VISIBLE_DEVICES=0 (máy dùng chung, chỉ GPU 0).")
    test = read("test")
    results, examples = [], {}
    for name, fn in systems():
        t0 = time.perf_counter()
        preds = [fn(w) for w, _ in test]
        ms = 1000 * (time.perf_counter() - t0) / len(test)
        scores = [score(p, refs) for p, (_, refs) in zip(preds, test, strict=True)]
        r = {
            "system": name,
            "exact": sum(s["exact"] for s in scores) / len(scores),
            "ser": sum(s["ser"] for s in scores) / len(scores),
            "cer": sum(s["cer"] for s in scores) / len(scores),
            "ms_per_word": ms,
        }
        results.append(r)
        examples[name] = preds
        print(
            f"{name:45s} đúng {r['exact']:6.1%}  SER {r['ser']:6.1%}  CER {r['cer']:6.1%}  {ms:.2f} ms/từ", flush=True
        )

    out = ROOT / "results"
    lines = [
        f"# Phiên âm từ nước ngoài: bộ test ({len(test)} từ chưa gặp khi huấn luyện)",
        "",
        "| Hệ thống | Đúng cả từ ↑ | Lỗi âm tiết (SER) ↓ | Lỗi ký tự (CER) ↓ | ms/từ |",
        "|---|---:|---:|---:|---:|",
    ]
    lines += [
        f"| {r['system']} | {r['exact']:.1%} | {r['ser']:.1%} | {r['cer']:.1%} | {r['ms_per_word']:.2f} |"
        for r in results
    ]
    lines += ["", "## Ví dụ (30 từ đầu của bộ test)", "", "| Từ | Đáp án | " + " | ".join(examples) + " |"]
    lines.append("|---|---|" + "---|" * len(examples))
    for i, (w, refs) in enumerate(test[:30]):
        lines.append(f"| {w} | {refs[0]} | " + " | ".join(clean_target(examples[n][i]) for n in examples) + " |")
    (out / "translit.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (out / "translit.json").write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
