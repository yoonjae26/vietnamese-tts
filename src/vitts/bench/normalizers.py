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


def _vitts_llm() -> Callable[[str], str]:
    """vitts với LLM làm bộ phiên âm (few-shot 20 ví dụ từ train). Bật bằng VITTS_LLM=<model id>."""
    import os
    import sys
    from pathlib import Path

    model_id = os.environ.get("VITTS_LLM")
    if not model_id:
        raise ImportError("đặt VITTS_LLM=<model id> để chạy")
    sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "training" / "translit"))
    from llm_baseline import LLMTransliterator, few_shot_examples
    from train import read

    from vitts.text import normalize_text

    llm = LLMTransliterator(model_id, shots=few_shot_examples(read("train"), k=20))
    return lambda text: normalize_text(text, translit=llm)


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
    "vitts + LLM translit": ("vitts-bench", _vitts_llm),
    "vinorm": ("vinorm", _vinorm),
    "soe-vinorm": ("soe-vinorm", _soe_vinorm),
    "vietnormalizer": ("vietnormalizer", _vietnormalizer),
}


def package_version(dist: str) -> str:
    try:
        return version(dist)
    except PackageNotFoundError:
        return "local"
