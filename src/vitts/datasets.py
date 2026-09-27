"""Formatter dataset tiếng Việt, dùng được trực tiếp với `TTS.tts.datasets.load_tts_samples`.

Mỗi formatter trả về list[dict] với các khóa `text`, `audio_file`, `speaker_name`, `root_path`,
đúng định dạng coqui-tts yêu cầu. Văn bản được chuẩn hóa bằng `normalize_text` ngay khi đọc,
nên có thể dùng `text_cleaner="basic_cleaners"` khi huấn luyện.
"""

import csv
import os
from pathlib import Path

from vitts.text import normalize_text


def vi_ljspeech(root_path: str, meta_file: str = "metadata.csv", **kwargs) -> list[dict]:  # noqa: ARG001
    """Định dạng giống LJSpeech: `wavs/<id>.wav` và `metadata.csv` với dòng `id|text` hoặc `id|text|speaker`."""
    items = []
    with open(os.path.join(root_path, meta_file), encoding="utf-8") as f:
        for line in f:
            cols = line.rstrip("\n").split("|")
            if len(cols) < 2 or not cols[1].strip():
                continue
            speaker = cols[2].strip() if len(cols) > 2 and cols[2].strip() else "default"
            wav = cols[0] if cols[0].endswith(".wav") else cols[0] + ".wav"
            items.append(
                {
                    "text": normalize_text(cols[1]),
                    "audio_file": os.path.join(root_path, "wavs", wav),
                    "speaker_name": speaker,
                    "root_path": root_path,
                }
            )
    return items


def vi_wav_txt_pairs(root_path: str, meta_file: str = "", **kwargs) -> list[dict]:  # noqa: ARG001
    """Thư mục chứa các cặp `abc.wav` + `abc.txt` (có thể lồng thư mục con).

    Tên thư mục con cấp một được dùng làm tên người nói.
    """
    root = Path(root_path)
    items = []
    for wav in sorted(root.rglob("*.wav")):
        txt = wav.with_suffix(".txt")
        if not txt.exists():
            continue
        text = txt.read_text(encoding="utf-8").strip()
        if not text:
            continue
        rel = wav.relative_to(root)
        speaker = rel.parts[0] if len(rel.parts) > 1 else "default"
        items.append(
            {
                "text": normalize_text(text),
                "audio_file": str(wav),
                "speaker_name": speaker,
                "root_path": root_path,
            }
        )
    return items


def vi_common_voice(root_path: str, meta_file: str = "validated.tsv", **kwargs) -> list[dict]:  # noqa: ARG001
    """Mozilla Common Voice (tiếng Việt).

    Common Voice phát hành file .mp3; hãy chuyển sang .wav trước (xem `scripts/prepare_common_voice.py`).
    Formatter này tìm file `clips_wav/<tên>.wav`.
    """
    items = []
    with open(os.path.join(root_path, meta_file), encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE):
            wav = os.path.join(root_path, "clips_wav", Path(row["path"]).with_suffix(".wav").name)
            items.append(
                {
                    "text": normalize_text(row["sentence"]),
                    "audio_file": wav,
                    "speaker_name": "cv_" + row["client_id"][:12],
                    "root_path": root_path,
                }
            )
    return items


FORMATTERS = {
    "vi_ljspeech": vi_ljspeech,
    "vi_wav_txt_pairs": vi_wav_txt_pairs,
    "vi_common_voice": vi_common_voice,
}
