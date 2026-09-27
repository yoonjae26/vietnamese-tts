import pytest

from vitts.text import CHARACTERS, PUNCTUATIONS, normalize_text, split_sentences


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("Xin Chào", "xin chào"),
        ("100k", "một trăm nghìn"),
        ("1.000.000đ", "một triệu đồng"),
        ("$5", "năm đô la"),
        ("36,5°C", "ba mươi sáu phẩy năm độ xê"),
        ("tăng 12%", "tăng mười hai phần trăm"),
        ("60km/h", "sáu mươi ki lô mét trên giờ"),
        ("14h30", "mười bốn giờ ba mươi phút"),
        ("lúc 7h sáng", "lúc bảy giờ sáng"),
        ("ngày 2/9/2024", "ngày hai tháng chín năm hai nghìn không trăm hai mươi tư"),
        ("tháng 4/2023", "tháng tư năm hai nghìn không trăm hai mươi ba"),
        ("thứ 4", "thứ tư"),
        ("từ 5-10 người", "từ năm đến mười người"),
        ("thắng 3-1", "thắng ba một"),
        ("Ngày 2/9/1945", "ngày hai tháng chín năm một nghìn chín trăm bốn mươi lăm"),
        ("23.450đ/lít", "hai mươi ba nghìn bốn trăm năm mươi đồng một lít"),
        ("5tr/tháng", "năm triệu một tháng"),
        ("50.000đ/kg", "năm mươi nghìn đồng một ki lô gam"),
        ("và/hoặc", "và hoặc"),
        ("tổng đài 1900 1234", "tổng đài một chín không không một hai ba bốn"),
        ("+84 912 345 678", "cộng tám tư chín một hai ba bốn năm sáu bảy tám"),
        ("0912 345 678", "không chín một hai ba bốn năm sáu bảy tám"),
        ("TP.HCM", "thành phố hồ chí minh"),
        ("UBND xã", "ủy ban nhân dân xã"),
        ("công nghệ AI", "công nghệ a i"),
        ("U23", "u hai mươi ba"),
        ("COVID-19", "cô vít mười chín"),
        ("hoà bình, thuỷ lợi, khoẻ", "hòa bình, thủy lợi, khỏe"),
        ("quý, hoàng", "quý, hoàng"),
        ("“Chào” (bạn)...", "chào bạn."),
        ("TIN NÓNG: GIÁ VÀNG TĂNG MẠNH", "tin nóng, giá vàng tăng mạnh"),
    ],
)
def test_normalize(raw, expected):
    assert normalize_text(raw) == expected


def test_nfd_input_becomes_nfc():
    import unicodedata

    assert normalize_text(unicodedata.normalize("NFD", "Việt Nam")) == "việt nam"


def test_output_only_uses_model_characters():
    allowed = set(CHARACTERS) | set(PUNCTUATIONS)
    out = normalize_text("Giá: 1.250.000₫ (≈ 50$) — liên hệ admin@example.com #sale 😀")
    assert set(out) <= allowed


def test_split_sentences_respects_max_chars():
    text = normalize_text("Câu thứ nhất. " + "một hai ba bốn năm " * 30 + ". Câu cuối!")
    chunks = split_sentences(text, max_chars=80)
    assert chunks[0] == "câu thứ nhất."
    assert chunks[-1] == "câu cuối!"
    assert all(len(c) <= 80 for c in chunks)
