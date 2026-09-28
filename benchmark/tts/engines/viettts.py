"""VietTTS (dangvansam/viet-tts, dựa trên CosyVoice), clone giọng từ audio mẫu.

- Giọng mẫu được nạp bằng `load_prompt_speech_from_file` của tác giả (tự cắt còn 3 đến 5 giây).
- Đặc trưng giọng mẫu (speech token, mel, speaker embedding) được trích một lần, giống cách
  làm với viXTTS và F5. `TTS.inference_tts` gốc trích lại ở mỗi câu, làm sai lệch RTF.
  Phần còn lại giữ nguyên luồng của tác giả: preprocess_text -> tách câu -> model.tts.
"""

import numpy as np
import torch
from huggingface_hub import snapshot_download
from viettts.tts import TTS
from viettts.utils.file_utils import load_prompt_speech_from_file

from engines.common import reference

REPO = "dangvansam/viet-tts"


class Engine:
    name = "VietTTS"
    license = "CC (see model card)"
    repo = REPO

    def __init__(self, device: str):  # noqa: ARG002
        # VietTTS tự chọn cuda nếu có; CUDA_VISIBLE_DEVICES=0 giới hạn nó ở GPU 0
        self.tts = TTS(model_dir=snapshot_download(REPO))
        prompt = load_prompt_speech_from_file(reference()[0])
        self.prompt_input = self.tts.frontend.frontend_tts("xin chào", prompt)
        self.sample_rate = 22050

    def synth(self, text: str, seed: int) -> np.ndarray:
        torch.manual_seed(seed)
        wavs = []
        for chunk in self.tts.frontend.preprocess_text(text, split=True):
            text_token, text_token_len = self.tts.frontend._extract_text_token(chunk)
            model_input = {**self.prompt_input, "text": text_token, "text_len": text_token_len}
            for out in self.tts.model.tts(**model_input, stream=False, speed=1.0):
                wavs.append(out["tts_speech"].squeeze(0).cpu().numpy())
        return np.concatenate(wavs).astype(np.float32)
