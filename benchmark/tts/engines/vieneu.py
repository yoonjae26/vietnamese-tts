"""VieNeu-TTS v3 Turbo (pnnbao-ump/VieNeu-TTS-v3-Turbo, 48 kHz), clone giọng từ audio mẫu.

Dùng SDK chính thức `vieneu` với tham số mặc định (theo README: `Vieneu()` + `add_voice`).
"""

import numpy as np
import torch
from vieneu import Vieneu

from engines.common import reference


class Engine:
    name = "VieNeu-TTS v3 Turbo"
    license = "Apache-2.0"
    repo = "pnnbao-ump/VieNeu-TTS-v3-Turbo"

    def __init__(self, device: str):
        self.tts = Vieneu(device="cuda" if device.startswith("cuda") else "cpu")
        self.tts.add_voice("benchmark_ref", reference()[0])
        self.sample_rate = self.tts.sample_rate

    def synth(self, text: str, seed: int) -> np.ndarray:
        torch.manual_seed(seed)
        np.random.seed(seed)
        audio = self.tts.infer(text, voice="benchmark_ref")
        return np.asarray(audio, dtype=np.float32).reshape(-1)
