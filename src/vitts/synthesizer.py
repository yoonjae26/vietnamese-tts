"""Bọc `TTS.api.TTS` của coqui-tts: chuẩn hóa văn bản, tách câu và ghép audio."""

import io
from dataclasses import dataclass

import numpy as np

from vitts.text import normalize_text, split_sentences

DEFAULT_MODEL = "tts_models/vie/fairseq/vits"  # Meta MMS, dùng được ngay không cần train


@dataclass
class Audio:
    samples: np.ndarray  # float32, mono, [-1, 1]
    sample_rate: int

    def to_wav_bytes(self) -> bytes:
        import soundfile as sf

        buf = io.BytesIO()
        sf.write(buf, self.samples, self.sample_rate, format="WAV", subtype="PCM_16")
        return buf.getvalue()


class VietnameseTTS:
    """Bộ đọc tiếng Việt.

    Dùng model có sẵn trên coqui (mặc định Meta MMS), hoặc checkpoint tự huấn luyện:

        tts = VietnameseTTS(model_path="best_model.pth", config_path="config.json")
        audio = tts.synthesize("Xin chào Việt Nam!")
    """

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
        model_path: str | None = None,
        config_path: str | None = None,
        gpu: bool = False,
        pause_ms: int = 150,
        max_chars: int = 200,
    ):
        from TTS.api import TTS  # import chậm để phần text dùng được mà không cần torch

        if model_path:
            self._tts = TTS(model_path=model_path, config_path=config_path, progress_bar=False, gpu=gpu)
            self.model_name = model_path
        else:
            self._tts = TTS(model_name, progress_bar=False, gpu=gpu)
            self.model_name = model_name
        self.sample_rate = self._tts.synthesizer.output_sample_rate
        self.pause_ms = pause_ms
        self.max_chars = max_chars

    def synthesize(self, text: str, speed: float = 1.0, speaker: str | None = None) -> Audio:
        chunks = split_sentences(normalize_text(text), self.max_chars)
        if not chunks:
            raise ValueError("Văn bản rỗng sau khi chuẩn hóa")

        silence = np.zeros(int(self.sample_rate * self.pause_ms / 1000), dtype=np.float32)
        pieces = []
        for chunk in chunks:
            wav = self._tts.tts(chunk, speaker=speaker, split_sentences=False)
            pieces += [np.asarray(wav, dtype=np.float32), silence]
        samples = np.concatenate(pieces[:-1])

        if speed != 1.0:
            import librosa

            samples = librosa.effects.time_stretch(samples, rate=speed)
        return Audio(np.clip(samples, -1.0, 1.0), self.sample_rate)

    @property
    def speakers(self) -> list[str]:
        return list(self._tts.speakers or [])
