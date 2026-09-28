"""IndexTTS-2 tiếng Việt (dinhthuan/index-tts-2-vietnamese), clone giọng từ audio mẫu.

Cài từ fork tiếng Việt: github.com/iamdinhthuan/index-tts-finetune-vietnamese
Tham số theo model card (use_fp16=True, use_cuda_kernel=False) và mặc định của `infer_vi.py`
(max_text_tokens=120, interval_silence=200).
"""

import numpy as np
import torch
from huggingface_hub import snapshot_download
from indextts.infer_v2 import IndexTTS2

from engines.common import reference

REPO = "dinhthuan/index-tts-2-vietnamese"


class Engine:
    name = "IndexTTS-2 Vietnamese"
    license = "Apache-2.0 (commercial use needs IndexTTS permission)"
    repo = REPO

    def __init__(self, device: str):
        model_dir = snapshot_download(REPO)
        self.tts = IndexTTS2(
            cfg_path=f"{model_dir}/config.yaml",
            model_dir=model_dir,
            use_fp16=device.startswith("cuda"),
            use_cuda_kernel=False,
            device=device,
        )
        self.ref = reference()[0]
        self.sample_rate = 22050

    def synth(self, text: str, seed: int) -> np.ndarray:
        torch.manual_seed(seed)
        sr, wav = self.tts.infer(
            spk_audio_prompt=self.ref,
            text=text,
            output_path=None,
            interval_silence=200,
            max_text_tokens_per_segment=120,
            verbose=False,
        )
        self.sample_rate = sr
        return (np.asarray(wav, dtype=np.float32).reshape(-1) / 32767.0).astype(np.float32)
