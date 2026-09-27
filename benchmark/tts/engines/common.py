"""Giọng mẫu dùng chung cho mọi model clone giọng (viXTTS, F5-TTS, VietTTS, VieNeu, IndexTTS).

Lấy 8.66 giây đầu của `samples/nu-luu-loat.wav` trong repo capleaf/viXTTS, cắt tại một
khoảng lặng để trọn câu. Lời thoại được PhoWhisper-large nghe lại rồi viết thành chữ đọc
("AI" -> "ây ai").
"""

from pathlib import Path

import soundfile as sf
from huggingface_hub import hf_hub_download

REF_SOURCE = ("capleaf/viXTTS", "samples/nu-luu-loat.wav")
REF_SECONDS = 8.66
REF_TEXT = (
    "xin chào, tôi là một trợ lý ây ai có khả năng trò chuyện với bạn bằng giọng nói tự nhiên, "
    "được phát triển bởi nhóm nón lá. tôi có thể hỗ trợ người khiếm thị."
)

_OUT = Path(__file__).resolve().parents[3] / "outputs" / "reference" / "ref_8s.wav"


def reference() -> tuple[str, str]:
    """Trả về (đường dẫn wav, lời thoại) của giọng mẫu, tạo file nếu chưa có."""
    if not _OUT.exists():
        wav, sr = sf.read(hf_hub_download(*REF_SOURCE), dtype="float32")
        _OUT.parent.mkdir(parents=True, exist_ok=True)
        sf.write(_OUT, wav[: int(REF_SECONDS * sr)], sr)
    return str(_OUT), REF_TEXT
