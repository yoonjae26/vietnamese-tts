"""Piper (VITS xuất ONNX, chạy CPU): giọng vi_VN-vais1000-medium trong rhasspy/piper-voices.

Piper được thiết kế cho CPU và thiết bị nhúng, nên benchmark chạy nó trên CPU (`--cpu`).
"""

import numpy as np
from huggingface_hub import hf_hub_download
from piper import PiperVoice
from piper.config import SynthesisConfig

REPO = "rhasspy/piper-voices"
VOICE = "vi/vi_VN/vais1000/medium/vi_VN-vais1000-medium.onnx"


class Engine:
    name = "Piper vi_VN-vais1000-medium"
    license = "CC-BY-4.0 (dữ liệu VAIS-1000)"
    repo = REPO

    def __init__(self, device: str):
        model = hf_hub_download(REPO, VOICE)
        config = hf_hub_download(REPO, VOICE + ".json")
        self.voice = PiperVoice.load(model, config, use_cuda=device.startswith("cuda"))
        self.sample_rate = self.voice.config.sample_rate

    def synth(self, text: str, seed: int) -> np.ndarray:  # noqa: ARG002 (Piper tất định)
        # Piper suy luận tất định trong ONNX (noise cố định theo config), seed không có tác dụng
        chunks = self.voice.synthesize(text, SynthesisConfig())
        return np.concatenate([c.audio_float_array for c in chunks]).astype(np.float32)
