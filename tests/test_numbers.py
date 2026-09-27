import pytest

from vitts.text.numbers import read_decimal, read_digits, read_number


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (0, "không"),
        (7, "bảy"),
        (10, "mười"),
        (11, "mười một"),
        (15, "mười lăm"),
        (20, "hai mươi"),
        (21, "hai mươi mốt"),
        (24, "hai mươi tư"),
        (25, "hai mươi lăm"),
        (100, "một trăm"),
        (101, "một trăm linh một"),
        (105, "một trăm linh năm"),
        (115, "một trăm mười lăm"),
        (1000, "một nghìn"),
        (1005, "một nghìn không trăm linh năm"),
        (1050, "một nghìn không trăm năm mươi"),
        (2024, "hai nghìn không trăm hai mươi tư"),
        (1_000_025, "một triệu không trăm hai mươi lăm"),
        (2_000_500, "hai triệu năm trăm"),
        (1_000_000_000, "một tỷ"),
        (5_000_000_000_000, "năm nghìn tỷ"),
        (-3, "âm ba"),
    ],
)
def test_read_number(n, expected):
    assert read_number(n) == expected


def test_read_digits():
    assert read_digits("0912") == "không chín một hai"


def test_read_decimal():
    assert read_decimal("3", "25") == "ba phẩy hai mươi lăm"
    assert read_decimal("0", "05") == "không phẩy không năm"
