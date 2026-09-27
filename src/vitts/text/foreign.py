"""Nhận diện từ nước ngoài, chữ viết tắt đọc được thành từ, và số La Mã.

Không dùng danh sách từ: quyết định dựa trên cấu trúc âm tiết tiếng Việt.

>>> [is_vietnamese_syllable(w) for w in ("tin", "nghieng", "quy", "show", "zoom", "online")]
[True, True, True, False, False, False]
>>> [is_pronounceable_acronym(w) for w in ("NATO", "UNESCO", "ATM", "FPT", "AI", "IELTS")]
[True, True, False, False, False, False]
>>> roman_to_int("XXI"), roman_to_int("IV"), roman_to_int("ABC")
(21, 4, None)
"""

import re

# Âm tiết tiếng Việt viết không dấu: [phụ âm đầu] + vần (nguyên âm/cụm nguyên âm) + [phụ âm cuối].
# Cho phép hơi rộng: thà coi nhầm một từ nước ngoài là tiếng Việt (giữ nguyên) còn hơn
# phiên âm nhầm một từ tiếng Việt.
_ONSET = r"(?:ngh|ng|gh|gi|kh|nh|ph|qu|th|tr|ch|[bcdđghklmnprstvx])?"
_NUCLEI = sorted(
    """a e i o u y ai ao au ay eo eu ia ie iu oa oe oi oo ua ue ui uo uu uy ye
       ieu yeu uoi uou oai oay oao oeo uay uya uye uyu""".split(),
    key=len,
    reverse=True,
)
_CODA = r"(?:ch|nh|ng|[cmnpt])?"
_RE_SYLLABLE = re.compile(rf"^{_ONSET}(?:{'|'.join(_NUCLEI)}){_CODA}$")
_VOWELS = set("aeiouy")


def is_vietnamese_syllable(word: str) -> bool:
    """`word` (chữ thường, không dấu) có thể là một âm tiết tiếng Việt viết không dấu không."""
    return bool(_RE_SYLLABLE.match(word.lower()))


def is_pronounceable_acronym(word: str) -> bool:
    """Chữ viết tắt in hoa thường được đọc thành từ (NATO, UNESCO) thay vì đánh vần (ATM, FPT).

    Quy tắc: từ 4 chữ cái, ít nhất 2 nguyên âm, không có 3 phụ âm liền nhau,
    và không bắt đầu bằng 2 phụ âm (trừ các cụm phát âm được như "st", "pr").
    """
    w = word.lower()
    if len(w) < 4 or sum(c in _VOWELS for c in w) < 2:
        return False
    if re.search(r"[^aeiouy]{3}", w):
        return False
    return w[0] in _VOWELS or w[1] in _VOWELS or w[:2] in {"bl", "br", "cl", "cr", "dr", "fl", "fr", "gl", "gr",
                                                            "pl", "pr", "sc", "sk", "sl", "sm", "sn", "sp", "st",
                                                            "sw", "tr"}  # fmt: skip


_ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}


def roman_to_int(s: str) -> int | None:
    """Số La Mã hợp lệ (I đến CCCXCIX) -> số nguyên, không hợp lệ -> None."""
    if not s or any(c not in _ROMAN for c in s):
        return None
    total = 0
    for i, c in enumerate(s):
        v = _ROMAN[c]
        total += -v if i + 1 < len(s) and _ROMAN[s[i + 1]] > v else v
    return total if _int_to_roman(total) == s else None


def _int_to_roman(n: int) -> str:
    out = ""
    for value, sym in (
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    ):
        while n >= value:
            out += sym
            n -= value
    return out
