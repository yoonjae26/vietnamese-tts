"""Chấm lại các hệ thống phiên âm trên bộ test nhiều đáp án do người duyệt "mù".

Đầu vào:
- outputs/review/predictions.json: output của từng hệ thống cho 150 từ (build_review.py)
- outputs/review/mapping.json: ứng viên nào đến từ hệ thống nào (người duyệt không thấy)
- thư mục kết quả duyệt xuất từ trang (mỗi từ một file JSON: accepted, custom, unsure)

Một từ được tính là đọc đúng nếu output của hệ thống nằm trong các cách đọc người duyệt chấp nhận
(ứng viên được chọn + cách đọc tự gõ). Từ đánh dấu "không chắc" bị bỏ qua.

    python training/translit/score_reviewed.py outputs/review/export
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(ROOT / "src"))

from prepare_data import clean_target  # noqa: E402

from vitts.bench.metrics import edit_distance  # noqa: E402

REVIEW = ROOT / "outputs" / "review"
SYSTEMS = {
    "vitts": "vitts translit (5.6M, beam 5)",
    "gpt-4o-mini_few-shot": "gpt-4o-mini few-shot",
    "gpt-4o-mini_zero-shot": "gpt-4o-mini zero-shot",
    "qwen2.5-7b_few-shot": "Qwen2.5-7B-Instruct few-shot",
    "vietnormalizer_rules": "vietnormalizer (quy tắc)",
    "gold": "Đáp án gốc của từ điển vietnormalizer",
}


def load_reviews(folder: Path) -> dict[str, dict]:
    out = {}
    for f in sorted(folder.rglob("*.json")):
        doc = json.loads(f.read_text(encoding="utf-8"))
        data = doc.get("data", doc)
        out[doc.get("id", f.stem)] = data
    return out


def main():
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else REVIEW / "export"
    reviews = load_reviews(folder)
    mapping = json.loads((REVIEW / "mapping.json").read_text(encoding="utf-8"))
    preds = json.loads((REVIEW / "predictions.json").read_text(encoding="utf-8"))
    items = {i["id"]: i for i in json.loads((REVIEW / "items.json").read_text(encoding="utf-8"))}

    accepted: dict[str, set[str]] = {}
    unsure = 0
    for wid, r in reviews.items():
        if r.get("unsure"):
            unsure += 1
            continue
        texts = {c["text"] for c in items[wid]["candidates"] if c["id"] in set(r.get("accepted", []))}
        texts |= {clean_target(t) for t in r.get("custom", []) if t.strip()}
        accepted[mapping[wid]["word"]] = texts

    words = sorted(accepted)
    no_valid = sum(1 for w in words if not accepted[w])
    print(
        f"đã duyệt {len(reviews)} từ | không chắc {unsure} | dùng để chấm {len(words)} | "
        f"từ không có cách đọc nào đúng {no_valid}"
    )

    rows = []
    for key, name in SYSTEMS.items():
        correct, ser = 0, 0.0
        for w in words:
            p = clean_target(preds[w].get(key, ""))
            refs = accepted[w]
            correct += p in refs
            if refs:
                ser += min(edit_distance(p.split(), r.split()) / max(len(r.split()), 1) for r in refs)
            else:
                ser += 1.0
        rows.append(
            {"system": name, "key": key, "exact": correct / len(words), "ser": ser / len(words), "n": len(words)}
        )
    rows.sort(key=lambda r: -r["exact"])

    lines = [
        f"# Phiên âm: bộ test nhiều đáp án do người duyệt ({len(words)} từ)",
        "",
        "Người duyệt chọn mọi cách đọc chấp nhận được trong các ứng viên đã xáo trộn, không biết ứng viên đến từ "
        "hệ thống nào (duyệt mù), và có thể tự gõ thêm. Một output được tính là đúng nếu nằm trong các cách đọc "
        f"được chấp nhận. Bỏ qua {unsure} từ đánh dấu không chắc.",
        "",
        "| Hệ thống | Đúng ↑ | Lỗi âm tiết ↓ |",
        "|---|---:|---:|",
    ]
    lines += [f"| {r['system']} | {r['exact']:.1%} | {r['ser']:.1%} |" for r in rows]
    (ROOT / "results" / "translit_reviewed.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (ROOT / "results" / "translit_reviewed.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    print("\n".join(lines))


if __name__ == "__main__":
    main()
