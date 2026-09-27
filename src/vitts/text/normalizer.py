"""Chuẩn hóa văn bản tiếng Việt trước khi đưa vào model TTS.

Biến văn bản "thô" thành chuỗi chỉ gồm chữ cái tiếng Việt thường và dấu câu cơ bản:

>>> normalize_text("Giá 100k, giao lúc 14h30 tại TP.HCM!")
'giá một trăm nghìn, giao lúc mười bốn giờ ba mươi phút tại thành phố hồ chí minh!'
"""

import re
import unicodedata
from collections.abc import Callable

from vitts.text.foreign import is_pronounceable_acronym, is_vietnamese_syllable, roman_to_int
from vitts.text.numbers import read_decimal, read_digits, read_number
from vitts.text.symbols import ALLOWED, TONE_MARKS

# --------------------------------------------------------------------------- #
# Từ điển viết tắt (phân biệt hoa thường)
# --------------------------------------------------------------------------- #
ABBREVIATIONS = {
    "TP.HCM": "thành phố hồ chí minh",
    "TP HCM": "thành phố hồ chí minh",
    "TPHCM": "thành phố hồ chí minh",
    "Tp.HCM": "thành phố hồ chí minh",
    "HCM": "hồ chí minh",
    "TP.": "thành phố",
    "Tp.": "thành phố",
    "TP": "thành phố",
    "HN": "hà nội",
    "VN": "việt nam",
    "UBND": "ủy ban nhân dân",
    "HĐND": "hội đồng nhân dân",
    "THPT": "trung học phổ thông",
    "THCS": "trung học cơ sở",
    "ĐH": "đại học",
    "CĐ": "cao đẳng",
    "GS.": "giáo sư",
    "PGS.": "phó giáo sư",
    "TS.": "tiến sĩ",
    "ThS.": "thạc sĩ",
    "BS.": "bác sĩ",
    "CSGT": "cảnh sát giao thông",
    "HLV": "huấn luyện viên",
    "SĐT": "số điện thoại",
    "BHXH": "bảo hiểm xã hội",
    "BHYT": "bảo hiểm y tế",
    "CMND": "chứng minh nhân dân",
    "CCCD": "căn cước công dân",
    "ĐHQG": "đại học quốc gia",
    "GD&ĐT": "giáo dục và đào tạo",
    "GDĐT": "giáo dục đào tạo",
    "CNTT": "công nghệ thông tin",
    "KHCN": "khoa học công nghệ",
    "KCN": "khu công nghiệp",
    "ĐBSCL": "đồng bằng sông cửu long",
    "TX.": "thị xã",
    "TT.": "thị trấn",
    "v.v.": "vân vân",
    "v.v": "vân vân",
    "OK": "ô kê",
    "COVID": "cô vít",
    "Covid": "cô vít",
}

LETTER_NAMES = {
    "a": "a", "b": "bê", "c": "xê", "d": "dê", "đ": "đê", "e": "e", "f": "ép",
    "g": "giê", "h": "hát", "i": "i", "j": "gi", "k": "ca", "l": "e lờ",
    "m": "em mờ", "n": "en nờ", "o": "o", "p": "pê", "q": "quy", "r": "e rờ",
    "s": "ét", "t": "tê", "u": "u", "v": "vê", "w": "vê kép", "x": "ích",
    "y": "i dài", "z": "dét",
}  # fmt: skip

# Đơn vị đứng sau số. Sắp xếp dài trước để "km/h" khớp trước "km".
UNITS = {
    "km/h": "ki lô mét trên giờ",
    "kWh": "ki lô oát giờ",
    "kW": "ki lô oát",
    "km²": "ki lô mét vuông",
    "km2": "ki lô mét vuông",
    "km": "ki lô mét",
    "cm": "xen ti mét",
    "mm": "mi li mét",
    "m²": "mét vuông",
    "m2": "mét vuông",
    "m³": "mét khối",
    "m3": "mét khối",
    "m": "mét",
    "kg": "ki lô gam",
    "mg": "mi li gam",
    "g": "gam",
    "ml": "mi li lít",
    "l": "lít",
    "ha": "héc ta",
    "°C": "độ xê",
    "°F": "độ ép",
    "°": "độ",
    "GB": "gi ga bai",
    "MB": "mê ga bai",
    "TB": "tê ra bai",
    "GHz": "gi ga héc",
    "Gbps": "gi ga bít trên giây",
    "Mbps": "mê ga bít trên giây",
    "kbps": "ki lô bít trên giây",
    "mAh": "mi li am pe giờ",
    "inch": "inh",
    "W": "oát",
    "MHz": "mê ga héc",
    "%": "phần trăm",
    "tr": "triệu",
    "k": "nghìn",
    "K": "nghìn",
    "VNĐ": "đồng",
    "VND": "đồng",
    "vnđ": "đồng",
    "đ": "đồng",
    "₫": "đồng",
    "USD": "đô la",
    "$": "đô la",
    "EUR": "ơ rô",
    "€": "ơ rô",
}

# --------------------------------------------------------------------------- #
# Regex
# --------------------------------------------------------------------------- #
_NUM = r"\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+(?:[.,]\d+)?"
_B = r"(?<![\w.,])"  # không dính với chữ/số phía trước
_E = r"(?![\w])"

_RE_DATE_DMY = re.compile(rf"(?:[Nn]gày\s+)?{_B}(\d{{1,2}})[/-](\d{{1,2}})[/-](\d{{4}}){_E}")
_RE_DATE_MY = re.compile(rf"(?<=tháng )(\d{{1,2}})[/-](\d{{4}}){_E}", re.IGNORECASE)
# "ngày 2/9", "tối 20/11", "đường 3/2" là ngày tháng; không có ngữ cảnh thì là phân số ("3/4" = ba phần bốn)
_DATE_CONTEXT = r"ngày|hôm|sáng|chiều|tối|trưa|đêm|mùng|mồng|đường|phố|lễ|dịp|từ|đến|trước|sau|vào|kỷ niệm"
_RE_DATE_DM = re.compile(rf"(?i)\b({_DATE_CONTEXT})\s+(\d{{1,2}})/(\d{{1,2}}){_E}")
_RE_FRACTION = re.compile(rf"{_B}(\d+)/(\d+){_E}")
_RE_HEIGHT = re.compile(rf"{_B}(\d)m(\d{{2}}){_E}")  # 1m75
_RE_NEGATIVE = re.compile(r"(?:(?<=\s)|^)-(?=\d)")  # -5°C (sau khi đã xử lý khoảng "5-10")
_RE_NUM_LETTER = re.compile(rf"{_B}(\d+)([A-ZĐ])(?![\w])")  # 15B, 4G
_RE_QUARTER = re.compile(r"\b([QP])\.\s?(?=\d|[A-ZĐÀ-Ỹ])")  # Q.1, P. Bến Thành
_RE_ROMAN = re.compile(r"(?i:\b(thế kỷ|thứ|khóa|khoá|đại hội|chương|phần))\s+([IVXLC]+)\b")
_RE_FOREIGN = re.compile(r"(?<![\w'])([A-Za-z]+)(?![\w'])")
_RE_TIME = re.compile(rf"{_B}(\d{{1,2}})(?::|h|g)(\d{{2}})(?::(\d{{2}}))?{_E}")
_RE_HOUR = re.compile(rf"{_B}(\d{{1,2}})(?:h|g){_E}")
_RE_PHONE = re.compile(rf"(?<![\w.,+])(\+84\s?|0)(\d[\d .]{{7,12}}\d){_E}")
_RE_HOTLINE = re.compile(rf"{_B}(1[89]00[\s.]?\d{{2,4}}(?:[\s.]?\d{{2,4}})?){_E}")
_RE_RANGE = re.compile(rf"{_B}({_NUM})\s*[-–]\s*({_NUM}){_E}")
_RE_CURRENCY_PREFIX = re.compile(rf"([$€])\s*({_NUM})")
_RE_UNIT = re.compile(
    rf"{_B}({_NUM})\s*(" + "|".join(re.escape(u) for u in sorted(UNITS, key=len, reverse=True)) + r")(?![\w²³])"
)
_RE_NUMBER = re.compile(_NUM)
_RE_ACRONYM_NUM = re.compile(r"\b([A-ZĐ]{1,5})(\d+)\b")
_RE_ACRONYM = re.compile(r"\b[A-ZĐ]{2,5}\b")
_RE_ABBR = re.compile(
    r"(?<!\w)(" + "|".join(re.escape(a) for a in sorted(ABBREVIATIONS, key=len, reverse=True)) + r")(?!\w)"
)

# "đồng/lít", "triệu/tháng" -> "đồng một lít", "triệu một tháng"
PER_WORDS = {
    "giây", "phút", "giờ", "ngày", "tuần", "tháng", "quý", "năm", "lít", "lượng", "chỉ", "tấn", "tạ",
    "người", "chiếc", "cái", "suất", "vé", "đêm", "lần", "hộp", "gói", "bao", "con", "kg", "g", "m", "m2", "km", "l",
}  # fmt: skip
_RE_PER = re.compile(r"(?<=[\w%])\s*/\s*(" + "|".join(sorted(PER_WORDS, key=len, reverse=True)) + r")(?!\w)")

_SPECIAL_ORDINALS = {  # "thứ 4" -> "thứ tư", "tháng 4" -> "tháng tư"
    ("thứ", "1"): "thứ nhất",
    ("thứ", "4"): "thứ tư",
    ("tháng", "4"): "tháng tư",
}
_RE_ORDINAL = re.compile(r"\b(thứ|tháng)\s+(1|4)\b", re.IGNORECASE)


# --------------------------------------------------------------------------- #
# Chuẩn hóa vị trí dấu thanh: kiểu cũ (hoà, thuỷ, khoẻ) -> kiểu mới (hòa, thủy, khỏe)
# --------------------------------------------------------------------------- #
def _build_tone_map() -> dict[str, str]:
    nfc = lambda s: unicodedata.normalize("NFC", s)  # noqa: E731
    mapping = {}
    for mark in TONE_MARKS.values():
        for first, second in (("o", "a"), ("o", "e"), ("u", "y")):
            mapping[first + nfc(second + mark)] = nfc(first + mark) + second
    return mapping


_TONE_MAP = _build_tone_map()
_RE_OLD_TONE = re.compile(r"(?<!q)(" + "|".join(_TONE_MAP) + r")(?!\w)")


def normalize_tone_placement(text: str) -> str:
    return _RE_OLD_TONE.sub(lambda m: _TONE_MAP[m.group(1)], text)


# --------------------------------------------------------------------------- #
# Đọc số
# --------------------------------------------------------------------------- #
def read_number_token(tok: str) -> str:
    """Đọc một chuỗi số theo quy ước Việt Nam: dấu chấm phân cách nghìn, dấu phẩy thập phân."""
    if re.fullmatch(r"\d{1,3}(?:\.\d{3})+(?:,\d+)?", tok):
        tok = tok.replace(".", "")
    if "," in tok:
        integer, fraction = tok.split(",", 1)
        return read_decimal(integer, fraction, "phẩy")
    if "." in tok:
        integer, fraction = tok.split(".", 1)
        return read_decimal(integer, fraction, "chấm")
    if len(tok) > 15 or (len(tok) > 1 and tok.startswith("0")):
        return read_digits(tok)
    return read_number(int(tok))


def _date_dmy(m: re.Match) -> str:
    d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if not (1 <= d <= 31 and 1 <= mo <= 12):
        return m.group(0)
    return f"ngày {read_number(d)} {_month(mo)} năm {read_number(y)}"


def _date_dm(m: re.Match) -> str:
    d, mo = int(m.group(2)), int(m.group(3))
    if not (1 <= d <= 31 and 1 <= mo <= 12):
        return m.group(0)
    return f"{m.group(1)} {read_number(d)} {_month(mo)}"


def _fraction(m: re.Match) -> str:
    return f"{read_number_token(m.group(1))} phần {read_number_token(m.group(2))}"


def _roman(m: re.Match) -> str:
    n = roman_to_int(m.group(2))
    if n is None:
        return m.group(0)
    word = m.group(1)
    if word.lower() == "thứ" and n in (1, 4):
        return f"{word} {'nhất' if n == 1 else 'tư'}"
    return f"{word} {read_number(n)}"


def _date_my(m: re.Match) -> str:
    mo, y = int(m.group(1)), int(m.group(2))
    if not 1 <= mo <= 12:
        return m.group(0)
    month = "tư" if mo == 4 else read_number(mo)
    return f"{month} năm {read_number(y)}"


def _month(mo: int) -> str:
    return "tháng tư" if mo == 4 else f"tháng {read_number(mo)}"


def _time(m: re.Match) -> str:
    h, mi = int(m.group(1)), int(m.group(2))
    if h > 24 or mi > 59:
        return m.group(0)
    out = f"{read_number(h)} giờ"
    if mi:
        out += f" {read_number(mi)} phút"
    if m.group(3) and int(m.group(3)):
        out += f" {read_number(int(m.group(3)))} giây"
    return out


def _hour(m: re.Match) -> str:
    h = int(m.group(1))
    return f"{read_number(h)} giờ" if h <= 24 else m.group(0)


def _range(m: re.Match) -> str:
    # "5-10" là khoảng ("năm đến mười"); "3-1" thường là tỉ số ("ba một")
    a, b = (float(g.replace(".", "").replace(",", ".")) for g in m.groups())
    return f"{m.group(1)} đến {m.group(2)}" if a < b else f"{m.group(1)} {m.group(2)}"


def _phone(m: re.Match) -> str:
    prefix = "cộng tám tư" if m.group(1).strip() == "+84" else "không"
    return f"{prefix} {read_digits(m.group(2))}"


def _spell(word: str) -> str:
    return " ".join(LETTER_NAMES.get(c, c) for c in word.lower())


def _acronym(word: str, translit: Callable[[str], str] | None) -> str:
    """NATO, UNESCO đọc thành từ (cần model phiên âm); ATM, FPT đánh vần."""
    if translit is not None and is_pronounceable_acronym(word):
        return translit(word.lower())
    return _spell(word)


def _foreign(m: re.Match, translit: Callable[[str], str]) -> str:
    word = m.group(1)
    if len(word) < 2 or word.isupper() or is_vietnamese_syllable(word):
        return word
    return translit(word.lower())


_DEFAULT_TRANSLIT: list = []


def default_transliterator() -> Callable[[str], str] | None:
    """Model phiên âm mặc định (models/translit/translit.pt) nếu có torch và checkpoint, không thì None."""
    if not _DEFAULT_TRANSLIT:
        try:
            from vitts.translit import DEFAULT_CHECKPOINT, Transliterator

            _DEFAULT_TRANSLIT.append(Transliterator.from_pretrained() if DEFAULT_CHECKPOINT.exists() else None)
        except ImportError:
            _DEFAULT_TRANSLIT.append(None)
    return _DEFAULT_TRANSLIT[0]


def _is_all_caps_text(text: str) -> bool:
    letters = [c for c in text if c.isalpha()]
    return len(letters) > 12 and all(c.isupper() for c in letters)


# --------------------------------------------------------------------------- #
# Pipeline chính
# --------------------------------------------------------------------------- #
def normalize_text(text: str, strict: bool = True, translit: Callable[[str], str] | str | None = None) -> str:
    """Chuẩn hóa văn bản tiếng Việt.

    Args:
        text: văn bản đầu vào.
        strict: bỏ mọi ký tự không nằm trong bảng ký tự của model.
        translit: hàm phiên âm từ nước ngoài ("iphone" -> "ai phôn"), hoặc "auto" để dùng model
            mặc định của vitts (cần torch). None: giữ nguyên từ nước ngoài, đánh vần mọi chữ viết tắt.
    """
    if translit == "auto":
        translit = default_transliterator()
    text = unicodedata.normalize("NFC", text)
    text = text.replace(" ", " ")
    text = re.sub(r"[“”„\"«»]", "", text)
    text = re.sub(r"[‘’`´]", "'", text)
    text = text.replace("…", ".").replace("—", ", ").replace("–", "-")

    text = _RE_ABBR.sub(lambda m: ABBREVIATIONS[m.group(1)], text)
    text = _RE_QUARTER.sub(lambda m: "quận " if m.group(1) == "Q" else "phường ", text)
    text = _RE_ROMAN.sub(_roman, text)

    # Số có ngữ cảnh: ngày, giờ, điện thoại, tiền, đơn vị, khoảng
    text = _RE_HOTLINE.sub(lambda m: read_digits(m.group(1)), text)
    text = _RE_PHONE.sub(_phone, text)
    text = _RE_DATE_DMY.sub(_date_dmy, text)
    text = _RE_DATE_MY.sub(_date_my, text)
    text = _RE_TIME.sub(_time, text)
    text = _RE_HOUR.sub(_hour, text)
    text = _RE_DATE_DM.sub(_date_dm, text)
    text = _RE_FRACTION.sub(_fraction, text)
    text = _RE_CURRENCY_PREFIX.sub(lambda m: f"{read_number_token(m.group(2))} {UNITS[m.group(1)]}", text)
    text = _RE_RANGE.sub(_range, text)
    text = _RE_NEGATIVE.sub("âm ", text)
    text = _RE_HEIGHT.sub(lambda m: f"{read_number(int(m.group(1)))} mét {read_number(int(m.group(2)))}", text)
    text = _RE_UNIT.sub(lambda m: f"{read_number_token(m.group(1))} {UNITS[m.group(2)]}", text)
    text = _RE_PER.sub(lambda m: f" một {UNITS.get(m.group(1), m.group(1))}", text)
    text = _RE_ORDINAL.sub(lambda m: _SPECIAL_ORDINALS[(m.group(1).lower(), m.group(2))], text)
    text = _RE_NUM_LETTER.sub(lambda m: f"{read_number_token(m.group(1))} {_spell(m.group(2))}", text)

    # Từ nước ngoài (iPhone, online): phiên âm. Từ viết hoa toàn bộ để bước chữ viết tắt xử lý,
    # nên output của hai bước không bao giờ bị xử lý lại.
    if translit is not None:
        text = _RE_FOREIGN.sub(lambda m: _foreign(m, translit), text)

    # Chữ viết tắt in hoa còn sót lại: đọc thành từ hoặc đánh vần (trừ khi cả đoạn văn viết hoa)
    if not _is_all_caps_text(text):
        text = _RE_ACRONYM_NUM.sub(lambda m: f"{_spell(m.group(1))} {read_number_token(m.group(2))}", text)
        text = _RE_ACRONYM.sub(lambda m: _acronym(m.group(0), translit), text)

    text = _RE_NUMBER.sub(lambda m: read_number_token(m.group(0)), text)

    text = text.lower()
    text = normalize_tone_placement(text)

    # Ký hiệu và dấu câu
    text = text.replace("&", " và ").replace("+", " cộng ").replace("=", " bằng ").replace("@", " a còng ")
    text = re.sub(r"[:;]", ",", text)
    text = re.sub(r"\s*\n+\s*", ". ", text)
    text = re.sub(r"(?<=\w)-(?=\w)", " ", text)
    text = re.sub(r"\s+-\s+", ", ", text)
    if strict:
        text = "".join(c if c in ALLOWED else " " for c in text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([,.!?])", r"\1", text)
    text = re.sub(r"([,.!?])[,.!?]+", r"\1", text)
    text = re.sub(r"^[,.!?\s-]+", "", text)
    return text.strip()


def split_sentences(text: str, max_chars: int = 200) -> list[str]:
    """Tách văn bản dài thành các đoạn ngắn để model đọc ổn định hơn."""
    chunks: list[str] = []
    for sentence in re.split(r"(?<=[.!?])\s+", text.strip()):
        if not sentence:
            continue
        if len(sentence) <= max_chars:
            chunks.append(sentence)
            continue
        current = ""
        for part in re.split(r"(?<=,)\s+", sentence):
            for word in part.split(" "):
                if current and len(current) + len(word) + 1 > max_chars:
                    chunks.append(current)
                    current = word
                else:
                    current = f"{current} {word}".strip()
        if current:
            chunks.append(current)
    return chunks
