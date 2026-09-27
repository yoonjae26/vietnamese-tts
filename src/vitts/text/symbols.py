"""Bảng ký tự tiếng Việt (dạng NFC) dùng cho tokenizer của model."""

import unicodedata

TONE_MARKS = {
    "huyền": "̀",
    "sắc": "́",
    "hỏi": "̉",
    "ngã": "̃",
    "nặng": "̣",
}

BASE_VOWELS = "aăâeêioôơuưy"


def _toned(vowel: str, mark: str) -> str:
    return unicodedata.normalize("NFC", vowel + mark)


TONED_VOWELS = "".join(_toned(v, m) for v in BASE_VOWELS for m in TONE_MARKS.values())

# Giữ đủ a-z (kể cả f, j, w, z) vì văn bản thực tế có nhiều từ mượn.
LETTERS = "abcdefghijklmnopqrstuvwxyz" + "ăâđêôơư" + TONED_VOWELS
PUNCTUATIONS = "!,.?-' "

# Ký tự đưa vào CharactersConfig khi huấn luyện
CHARACTERS = "".join(sorted(set(LETTERS)))
ALLOWED = set(CHARACTERS) | set(PUNCTUATIONS)
