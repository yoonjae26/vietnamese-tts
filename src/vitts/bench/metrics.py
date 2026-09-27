"""Chấm điểm output chuẩn hóa so với đáp án.

So sánh ở mức "cách đọc": bỏ dấu câu, hoa/thường, vị trí dấu thanh (hoà = hòa)
và quy các biến thể vùng miền về một dạng, vì chúng đọc ra đều đúng.
"""

import re
import unicodedata

from vitts.text.normalizer import normalize_tone_placement

# Biến thể được coi là tương đương (áp dụng trên chuỗi đã tách từ bằng dấu cách)
VARIANTS = [
    (r"\bngàn\b", "nghìn"),
    (r"\blẻ\b", "linh"),
    (r"\btỉ\b", "tỷ"),
    (r"\bmươi bốn\b", "mươi tư"),
    (r"\bnhăm\b", "lăm"),
    (r"\bngày (mùng|mồng) ", "ngày "),
    (r"\bxăng ti\b", "xen ti"),
    (r"\bđô la mỹ\b", "đô la"),
    (r"\bgiê\b", "gi"),
    (r"\bkí lô\b", "ki lô"),
    (r"\bghi ga\b", "gi ga"),
    (r"\bga bay\b", "ga bai"),
    (r"\btháng bốn\b", "tháng tư"),
    (r"\bviệt nam đồng\b", "đồng"),
]
_VARIANTS = [(re.compile(p), r) for p, r in VARIANTS]


def canonicalize(text: str) -> str:
    text = unicodedata.normalize("NFC", text).lower()
    text = normalize_tone_placement(text)
    text = re.sub(r"[^\w\s]|_", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    for pattern, repl in _VARIANTS:
        text = pattern.sub(repl, text)
    return text


def edit_distance(a: list[str], b: list[str]) -> int:
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        for j, y in enumerate(b, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (x != y))
        prev = cur
    return prev[-1]


def score(hypothesis: str, references: list[str]) -> tuple[int, int]:
    """Trả về (số lỗi từ, số từ của đáp án gần nhất). WER = lỗi / số từ."""
    hyp = canonicalize(hypothesis).split()
    best = None
    for ref in references:
        r = canonicalize(ref).split()
        cand = (edit_distance(hyp, r), len(r))
        if best is None or cand[0] / max(cand[1], 1) < best[0] / max(best[1], 1):
            best = cand
    return best
