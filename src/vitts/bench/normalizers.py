"""Adapter thống nhất cho các bộ chuẩn hóa văn bản tiếng Việt.

Mỗi adapter là một hàm `str -> str`. Thư viện ngoài chỉ được import khi cần,
để thiếu một thư viện không làm hỏng cả benchmark.
"""

from collections.abc import Callable
from importlib.metadata import PackageNotFoundError, version


def _vitts() -> Callable[[str], str]:
    from vitts.text import normalize_text

    return normalize_text


def _vitts_translit() -> Callable[[str], str]:
    from vitts.text import normalize_text
    from vitts.text.normalizer import default_transliterator

    translit = default_transliterator()
    if translit is None:
        raise ImportError("cần torch và models/translit/translit.pt")
    return lambda text: normalize_text(text, translit=translit)


def _vinorm() -> Callable[[str], str]:
    from vinorm import TTSnorm

    return lambda text: TTSnorm(text)


def _soe_vinorm() -> Callable[[str], str]:
    from soe_vinorm import SoeNormalizer

    return SoeNormalizer().normalize


def _vietnormalizer() -> Callable[[str], str]:
    from vietnormalizer import VietnameseNormalizer

    return VietnameseNormalizer().normalize


NORMALIZERS: dict[str, tuple[str, Callable[[], Callable[[str], str]]]] = {
    # tên hiển thị: (tên gói trên PyPI, hàm khởi tạo)
    "vitts (ours)": ("vitts-bench", _vitts),
    "vitts + translit (ours)": ("vitts-bench", _vitts_translit),
    "vinorm": ("vinorm", _vinorm),
    "soe-vinorm": ("soe-vinorm", _soe_vinorm),
    "vietnormalizer": ("vietnormalizer", _vietnormalizer),
}


def package_version(dist: str) -> str:
    try:
        return version(dist)
    except PackageNotFoundError:
        return "local"
