"""Chấm các checkpoint phiên âm trên 149 từ đã được người duyệt mù (data/translit/review/).

    CUDA_VISIBLE_DEVICES=0 python training/translit/eval_reviewed_models.py \
        V0=models/translit/translit.pt V1=models/translit/gpt.pt V2=models/translit/both.pt

In ra độ chính xác theo người duyệt, khoảng tin cậy 95% (bootstrap), và so theo cặp với gpt-4o-mini
few-shot trên cùng từng từ.
"""

import json
import os
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).parent))

from prepare_data import clean_target  # noqa: E402

REVIEW = ROOT / "data" / "translit" / "review"
B = 5000


def accepted_sets() -> dict[str, set[str]]:
    items = {i["id"]: i for i in json.loads((REVIEW / "items.json").read_text(encoding="utf-8"))}
    out = {}
    for line in (REVIEW / "reviews.jsonl").read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        if r["unsure"]:
            continue
        texts = {c["text"] for c in items[r["id"]]["candidates"] if c["id"] in r["accepted"]}
        out[r["word"]] = texts | {clean_target(t) for t in r["custom"] if t.strip()}
    return out


def ci(xs: list[float], rng) -> tuple[float, float]:
    bs = sorted(sum(rng.choice(xs) for _ in xs) / len(xs) for _ in range(B))
    return bs[int(0.025 * B)], bs[int(0.975 * B)]


def main():
    if os.environ.get("CUDA_VISIBLE_DEVICES") != "0":
        sys.exit("Cần CUDA_VISIBLE_DEVICES=0 (máy dùng chung, chỉ GPU 0).")
    from vitts.translit import Transliterator

    acc = accepted_sets()
    words = sorted(acc)
    preds = json.loads((REVIEW / "predictions.json").read_text(encoding="utf-8"))
    systems = {"gpt-4o-mini few-shot": [clean_target(preds[w]["gpt-4o-mini_few-shot"]) for w in words]}
    for arg in sys.argv[1:]:
        name, path = arg.split("=", 1)
        t = Transliterator.from_pretrained(path, device="cuda:0", beam=5)
        systems[name] = [clean_target(t(w)) for w in words]

    rng = random.Random(0)
    correct = {n: [p in acc[w] for p, w in zip(ps, words, strict=True)] for n, ps in systems.items()}
    ref = correct["gpt-4o-mini few-shot"]
    rows = []
    for name, c in correct.items():
        lo, hi = ci(c, rng)
        row = {"system": name, "acc": sum(c) / len(c), "ci": [lo, hi]}
        if name != "gpt-4o-mini few-shot":
            d = [int(x) - int(y) for x, y in zip(c, ref, strict=True)]
            dlo, dhi = ci(d, rng)
            row["vs_gpt"] = {"diff": sum(d) / len(d), "ci": [dlo, dhi]}
        rows.append(row)
        extra = f" | so với GPT {row['vs_gpt']['diff']:+.1%} [{dlo:+.1%}, {dhi:+.1%}]" if "vs_gpt" in row else ""
        print(f"{name:24s} {row['acc']:.1%} [{lo:.1%}, {hi:.1%}]{extra}", flush=True)
    out = ROOT / "results" / "translit_reviewed_models.json"
    out.write_text(json.dumps({"n": len(words), "rows": rows}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("DONE", out)


if __name__ == "__main__":
    main()
