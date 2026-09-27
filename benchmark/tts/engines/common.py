"""Giọng mẫu dùng chung cho mọi model clone giọng (viXTTS, F5-TTS, VietTTS, VieNeu, IndexTTS).

`reference/yoonjae26.wav`: giọng thật của tác giả repo (yoonjae26), đồng ý công khai để làm benchmark.
Ghi âm bằng điện thoại (m4a, 48 kHz), chuyển sang mono 24 kHz, cắt 8.05 giây tại khoảng lặng sau
"hồ chí minh" và chuẩn hóa đỉnh âm lượng về 0.9 (bản gốc rất nhỏ, đỉnh khoảng 0.04).
Lời thoại do PhoWhisper-large chép lại và đã được tác giả xác nhận.
"""

from pathlib import Path

REF_WAV = Path(__file__).resolve().parents[1] / "reference" / "yoonjae26.wav"
REF_TEXT = (
    "xin chào việt nam, giá một trăm ngàn, giao lúc bốn giờ ba mươi phút ngày hai tháng chín tại thành phố hồ chí minh."
)


def reference() -> tuple[str, str]:
    """Trả về (đường dẫn wav, lời thoại) của giọng mẫu."""
    return str(REF_WAV), REF_TEXT
