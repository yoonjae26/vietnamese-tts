"""F5-TTS-Vietnamese-1000h (hynt/F5-TTS-Vietnamese-ViVoice), clone giọng từ audio mẫu.

Cài: pip install -e github.com/nguyenthienhy/F5-TTS-Vietnamese
Tham số theo lệnh mẫu của tác giả: model F5TTS_Base, vocoder vocos, speed 1.0 (nfe_step mặc định 32).
"""

import shutil
from pathlib import Path

import numpy as np
from f5_tts.api import F5TTS
from f5_tts.infer.utils_infer import infer_process, preprocess_ref_audio_text
from f5_tts.model.utils import seed_everything
from huggingface_hub import hf_hub_download

from engines.common import reference

REPO = "hynt/F5-TTS-Vietnamese-ViVoice"


class Engine:
    name = "F5-TTS-Vietnamese-1000h"
    license = "CC-BY-NC-SA-4.0"
    repo = REPO

    def __init__(self, device: str):
        ckpt = hf_hub_download(REPO, "model_last.pt")
        # Repo lưu vocab dưới tên config.json; tác giả hướng dẫn đổi tên thành vocab.txt
        vocab = Path(ckpt).with_name("vocab.txt")
        if not vocab.exists():
            shutil.copy(hf_hub_download(REPO, "config.json"), vocab)
        self.model = F5TTS(model="F5TTS_Base", ckpt_file=ckpt, vocab_file=str(vocab), device=device)
        self.device = device
        self.sample_rate = self.model.target_sample_rate
        # Xử lý giọng mẫu một lần (F5TTS.infer làm lại việc này ở mỗi lần gọi, làm sai lệch RTF)
        ref_audio, ref_text = reference()
        self.ref_audio, self.ref_text = preprocess_ref_audio_text(ref_audio, ref_text, show_info=_quiet, device=device)

    def synth(self, text: str, seed: int) -> np.ndarray:
        seed_everything(seed)
        wav, _sr, _spec = infer_process(
            self.ref_audio,
            self.ref_text,
            text,
            self.model.ema_model,
            self.model.vocoder,
            self.model.mel_spec_type,
            show_info=_quiet,
            progress=None,
            speed=1.0,
            nfe_step=32,
            device=self.device,
        )
        return np.asarray(wav, dtype=np.float32)


def _quiet(*args, **kwargs):
    pass
