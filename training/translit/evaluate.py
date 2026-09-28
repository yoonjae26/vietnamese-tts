"""Đánh giá phiên âm từ nước ngoài trên bộ test (từ chưa gặp khi huấn luyện).

    CUDA_VISIBLE_DEVICES=0 python training/translit/evaluate.py
    CUDA_VISIBLE_DEVICES=0 python training/translit/evaluate.py --llm Qwen/Qwen2.5-7B-Instruct

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


def systems(llm: str | None):
    import torch

    from vitts.translit import Transliterator

    yield "Keep English spelling", lambda w: w

    from vietnormalizer.transliterator import transliterate_word

    yield "vietnormalizer (rules, no dictionary lookup)", transliterate_word

    from soe_vinorm import SoeNormalizer

    soe = SoeNormalizer()
    yield "soe-vinorm", lambda w: soe.normalize(w)

    greedy = Transliterator.from_pretrained(device="cuda:0", beam=1)
    greedy.params = sum(p.numel() for p in greedy.model.parameters())
    yield "vitts translit (greedy)", greedy
    beam = Transliterator.from_pretrained(device="cuda:0", beam=5)
    beam.params = greedy.params
    yield "vitts translit (beam 5)", beam

    if llm:
        from llm_baseline import LLMTransliterator, few_shot_examples

        del greedy, beam
        torch.cuda.empty_cache()
        model = LLMTransliterator(llm)
        short = llm.split("/")[-1]
        yield f"{short} zero-shot", model
        model.shots, model.cache = few_shot_examples(read("train"), k=20), {}
        yield f"{short} few-shot (20 examples from train)", model


def main():
    import os

    if os.environ.get("CUDA_VISIBLE_DEVICES") != "0":
        sys.exit("Cần CUDA_VISIBLE_DEVICES=0 (máy dùng chung, chỉ GPU 0).")
    import argparse

    import torch

    parser = argparse.ArgumentParser()
    parser.add_argument("--llm", help="model id trên Hugging Face, ví dụ Qwen/Qwen2.5-7B-Instruct")
    args = parser.parse_args()

    test = read("test")
    results, examples = [], {}
    for name, fn in systems(args.llm):
        torch.cuda.reset_peak_memory_stats()
        t0 = time.perf_counter()
        words = [w for w, _ in test]
        preds = fn.batch(words) if hasattr(fn, "batch") else [fn(w) for w in words]  # LLM: sinh theo lô
        ms = 1000 * (time.perf_counter() - t0) / len(test)
        scores = [score(p, refs) for p, (_, refs) in zip(preds, test, strict=True)]
        r = {
            "system": name,
            "exact": sum(s["exact"] for s in scores) / len(scores),
            "ser": sum(s["ser"] for s in scores) / len(scores),
            "cer": sum(s["cer"] for s in scores) / len(scores),
            "ms_per_word": ms,
            "params": getattr(fn, "params", None),
            "peak_vram_gb": torch.cuda.max_memory_allocated() / 1e9 if hasattr(fn, "params") else None,
        }
        results.append(r)
        examples[name] = preds
        print(
            f"{name:45s} đúng {r['exact']:6.1%}  SER {r['ser']:6.1%}  CER {r['cer']:6.1%}  {ms:.2f} ms/từ", flush=True
        )

    out = ROOT / "results"
    lines = [
        f"# Loanword transliteration: test set ({len(test)} words unseen in training)",
        "",
        "| System | Params | Exact match ↑ | Syllable error (SER) ↓ | Character error (CER) ↓ | ms/word | VRAM |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]

    def fmt_params(n):
        return "–" if n is None else f"{n / 1e9:.1f}B" if n >= 1e9 else f"{n / 1e6:.1f}M"

    def fmt_vram(gb):
        return "–" if gb is None else f"{gb:.1f} GB"

    lines += [
        f"| {r['system']} | {fmt_params(r['params'])} | {r['exact']:.1%} | {r['ser']:.1%} | {r['cer']:.1%} "
        f"| {r['ms_per_word']:.2f} | {fmt_vram(r['peak_vram_gb'])} |"
        for r in results
    ]
    lines += [
        "",
        "vitts decodes one word at a time; LLMs generate in batches of 64 words on GPU "
        "(ms/word is the average over the whole set).",
    ]
    lines += ["", "## Examples (first 30 test words)", "", "| Word | Reference | " + " | ".join(examples) + " |"]
    lines.append("|---|---|" + "---|" * len(examples))
    for i, (w, refs) in enumerate(test[:30]):
        lines.append(f"| {w} | {refs[0]} | " + " | ".join(clean_target(examples[n][i]) for n in examples) + " |")
    (out / "translit.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (out / "translit.json").write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
