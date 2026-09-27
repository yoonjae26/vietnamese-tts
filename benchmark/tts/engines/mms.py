"""Meta MMS-TTS tiếng Việt (VITS, một giọng)."""

import numpy as np
import torch
from transformers import VitsModel, VitsTokenizer, set_seed

REPO = "facebook/mms-tts-vie"


class Engine:
    name = "MMS-TTS (Meta)"
    license = "CC-BY-NC-4.0"
    repo = REPO

    def __init__(self, device: str):
        self.device = device
        self.tokenizer = VitsTokenizer.from_pretrained(REPO)
        self.model = VitsModel.from_pretrained(REPO).to(device).eval()
        self.sample_rate = self.model.config.sampling_rate

    @torch.inference_mode()
    def synth(self, text: str, seed: int) -> np.ndarray:
        set_seed(seed)  # VITS có bộ dự đoán thời lượng ngẫu nhiên
        inputs = self.tokenizer(text, return_tensors="pt").to(self.device)
        wav = self.model(**inputs).waveform[0]
        return wav.float().cpu().numpy()
