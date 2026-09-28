"""Chạy benchmark chuẩn hóa văn bản và ghi kết quả vào `results/`.

python benchmark/normalization/run.py --split heldout      # con số công bố chính
python benchmark/normalization/run.py --split dev --only vinorm soe-vinorm
"""

import argparse
import json
import platform
import time
from collections import defaultdict
from datetime import date
from pathlib import Path

from vitts.bench.metrics import canonicalize, score
from vitts.bench.normalizers import NORMALIZERS, package_version

ROOT = Path(__file__).resolve().parents[2]
SPLITS = {"dev": "testset.jsonl", "heldout": "testset_heldout.jsonl", "heldout_v2": "testset_heldout_v2.jsonl"}


def run_one(name: str, cases: list[dict]) -> dict:
    dist, factory = NORMALIZERS[name]
    fn = factory()
    fn(cases[0]["input"])  # warm-up (tải model / từ điển)

    per_case = []
    start = time.perf_counter()
    for case in cases:
        try:
            out = fn(case["input"])
        except Exception as e:  # một câu lỗi không được làm dừng cả benchmark
            out = f"<ERROR {type(e).__name__}: {e}>"
        errors, n_words = score(out, case["references"])
        per_case.append({**case, "output": out, "errors": errors, "ref_words": n_words, "exact": errors == 0})
    elapsed = time.perf_counter() - start
    return {"name": name, "version": package_version(dist), "seconds": elapsed, "cases": per_case}


def summarize(result: dict) -> dict:
    by_cat = defaultdict(lambda: {"n": 0, "exact": 0, "errors": 0, "words": 0})
    for c in result["cases"]:
        for key in (c["category"], "ALL"):
            s = by_cat[key]
            s["n"] += 1
            s["exact"] += c["exact"]
            s["errors"] += c["errors"]
            s["words"] += c["ref_words"]
    return {
        cat: {"accuracy": s["exact"] / s["n"], "wer": s["errors"] / max(s["words"], 1), "n": s["n"]}
        for cat, s in by_cat.items()
    }


def to_markdown(
    results: list[dict], summaries: dict[str, dict], categories: list[str], split: str, run_date: str | None = None
) -> str:
    names = [r["name"] for r in results]
    lines = [
        f"# Text normalization: `{split}` set ({run_date or date.today().isoformat()})",
        "",
        f"{len(results[0]['cases'])} sentences, Python {platform.python_version()}.",
        "Cells: **sentences normalized exactly right** (WER in brackets). Best in bold.",
        "",
        "| Category | n | " + " | ".join(f"{r['name']} `{r['version']}`" for r in results) + " |",
        "|---|---:|" + "---:|" * len(results),
    ]
    for cat in [*categories, "ALL"]:
        accs = [summaries[n][cat]["accuracy"] for n in names]
        best = max(accs)
        cells = []
        for n in names:
            s = summaries[n][cat]
            cell = f"{s['accuracy']:.0%} ({s['wer']:.1%})"
            cells.append(f"**{cell}**" if s["accuracy"] == best else cell)
        label = "**Total**" if cat == "ALL" else cat
        lines.append(f"| {label} | {summaries[names[0]][cat]['n']} | " + " | ".join(cells) + " |")
    lines += [
        "| ms / sentence | | " + " | ".join(f"{1000 * r['seconds'] / len(r['cases']):.1f}" for r in results) + " |",
        "",
    ]
    return "\n".join(lines)


def write_errors(path: Path, results: list[dict]) -> None:
    """Every wrong sentence per system, to help improve the normalizers."""
    with path.open("w", encoding="utf-8") as f:
        for r in results:
            wrong = [c for c in r["cases"] if not c["exact"]]
            f.write(f"## {r['name']}: {len(wrong)} wrong\n\n| id | input | output | reference |\n|---|---|---|---|\n")
            for c in wrong:
                cells = [c["id"], c["input"], canonicalize(c["output"]), canonicalize(c["references"][0])]
                f.write("| " + " | ".join(x.replace("|", "\\|") for x in cells) + " |\n")
            f.write("\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--split", choices=list(SPLITS), default="heldout")
    parser.add_argument("--only", nargs="*", choices=list(NORMALIZERS), help="chỉ chạy các bộ này")
    parser.add_argument("--out", default=str(ROOT / "results"))
    args = parser.parse_args()

    testset = Path(__file__).with_name(SPLITS[args.split])
    cases = [json.loads(line) for line in testset.read_text(encoding="utf-8").splitlines() if line.strip()]
    categories = list(dict.fromkeys(c["category"] for c in cases))

    results = []
    for name in args.only or NORMALIZERS:
        try:
            results.append(run_one(name, cases))
            print(f"✓ {name}")
        except ImportError as e:
            print(f"✗ bỏ qua {name}: {e}")

    summaries = {r["name"]: summarize(r) for r in results}
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    md = to_markdown(results, summaries, categories, args.split)
    (out / f"normalization_{args.split}.md").write_text(md, encoding="utf-8")
    (out / f"normalization_{args.split}.json").write_text(
        json.dumps({"summary": summaries, "results": results}, ensure_ascii=False, indent=1), encoding="utf-8"
    )

    write_errors(out / f"normalization_{args.split}_errors.md", results)
    print(md)


if __name__ == "__main__":
    main()
