"""Chuẩn bị dữ liệu phiên âm từ nước ngoài -> tiếng Việt.

Nguồn: `non-vietnamese-words.csv` của vietnormalizer (MIT, xem data/translit/LICENSE-vietnormalizer),
17.7k cặp viết tay như "container -> công-tê-nơ".

- Làm sạch: chữ thường, Unicode NFC, thống nhất vị trí dấu thanh, gạch nối -> dấu cách.
- Chia train/dev/test 80/10/10 THEO GỐC TỪ (container, containers, container's cùng một phần),
  để bộ test đo khả năng đọc từ chưa gặp chứ không phải học thuộc biến thể.

    python training/translit/prepare_data.py
"""

import csv
import hashlib
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from vitts.text.normalizer import normalize_tone_placement  # noqa: E402

OUT = ROOT / "data" / "translit"
SUFFIXES = ("'s", "ies", "es", "s", "ed", "ing", "ers", "er")


def find_source() -> Path:
    import vietnormalizer

    return Path(vietnormalizer.__file__).parent / "data" / "non-vietnamese-words.csv"


def clean_target(t: str) -> str:
    t = unicodedata.normalize("NFC", t).lower().replace("-", " ")
    t = normalize_tone_placement(re.sub(r"\s+", " ", t).strip())
    return t


def stem(word: str) -> str:
    for suf in SUFFIXES:
        if word.endswith(suf) and len(word) - len(suf) >= 3:
            return word[: -len(suf)]
    return word


def split_of(word: str) -> str:
    h = int(hashlib.md5(stem(word).encode()).hexdigest(), 16) % 100
    return "train" if h < 80 else "dev" if h < 90 else "test"


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else find_source()
    pairs = defaultdict(list)
    with open(src, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            word = row["original"].strip().lower()
            target = clean_target(row["transliteration"])
            if not re.fullmatch(r"[a-z][a-z'.\- ]*", word) or not target:
                continue
            if re.search(r"[a-z]{6,}", target) and target.replace(" ", "") == word:  # chưa phiên âm
                continue
            if target not in pairs[word]:
                pairs[word].append(target)

    OUT.mkdir(parents=True, exist_ok=True)
    files = {s: open(OUT / f"{s}.tsv", "w", encoding="utf-8") for s in ("train", "dev", "test")}
    counts = defaultdict(int)
    for word in sorted(pairs):
        s = split_of(word)
        # một từ có thể có nhiều cách đọc đúng: ghi tất cả, ngăn bằng " | "
        files[s].write(f"{word}\t{' | '.join(pairs[word])}\n")
        counts[s] += 1
    for f in files.values():
        f.close()
    print(f"nguồn: {src}")
    print(" ".join(f"{s}={counts[s]}" for s in ("train", "dev", "test")), f"tổng={sum(counts.values())}")


if __name__ == "__main__":
    main()
