"""Đọc số thành chữ tiếng Việt.

>>> read_number(21)
'hai mươi mốt'
>>> read_number(105)
'một trăm linh năm'
>>> read_number(1_000_025)
'một triệu không trăm hai mươi lăm'
"""

DIGITS = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]

# Hậu tố cho nhóm 3 chữ số thứ i (tính từ phải): "", nghìn, triệu, tỷ, nghìn tỷ, ...
_GROUP_BASE = ["", "nghìn", "triệu"]


def _group_suffix(index: int) -> str:
    parts = [_GROUP_BASE[index % 3]] + ["tỷ"] * (index // 3)
    return " ".join(p for p in parts if p)


def _read_triple(n: int, full: bool) -> list[str]:
    """Đọc một nhóm 0..999.

    `full=True` khi nhóm này đứng sau một nhóm lớn hơn, khi đó phải đọc đủ
    "không trăm" / "linh" (vd. 1005 -> "một nghìn không trăm linh năm").
    """
    hundreds, rest = divmod(n, 100)
    tens, units = divmod(rest, 10)
    words: list[str] = []

    if full or hundreds:
        words += [DIGITS[hundreds], "trăm"]

    if tens == 0:
        if units:
            if words:
                words.append("linh")
            words.append(DIGITS[units])
    elif tens == 1:
        words.append("mười")
        if units == 5:
            words.append("lăm")
        elif units:
            words.append(DIGITS[units])
    else:
        words += [DIGITS[tens], "mươi"]
        if units == 1:
            words.append("mốt")
        elif units == 4:
            words.append("tư")
        elif units == 5:
            words.append("lăm")
        elif units:
            words.append(DIGITS[units])
    return words


def read_number(n: int) -> str:
    """Đọc một số nguyên (có thể âm) thành chữ."""
    if n < 0:
        return "âm " + read_number(-n)
    if n == 0:
        return DIGITS[0]

    groups = []
    while n:
        n, g = divmod(n, 1000)
        groups.append(g)

    words: list[str] = []
    for index in range(len(groups) - 1, -1, -1):
        g = groups[index]
        if g == 0:
            continue
        words += _read_triple(g, full=bool(words))
        suffix = _group_suffix(index)
        if suffix:
            words.append(suffix)
    return " ".join(words)


def read_digits(s: str) -> str:
    """Đọc từng chữ số, dùng cho số điện thoại, mã số, phần thập phân có số 0 đứng đầu."""
    return " ".join(DIGITS[int(c)] for c in s if c.isdigit())


def read_decimal(integer: str, fraction: str, sep_word: str = "phẩy") -> str:
    """Đọc số thập phân, vd. ("3", "25") -> "ba phẩy hai mươi lăm"."""
    frac = read_digits(fraction) if fraction.startswith("0") else read_number(int(fraction))
    return f"{read_number(int(integer))} {sep_word} {frac}"
