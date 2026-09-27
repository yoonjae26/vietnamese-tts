"""viXTTS: XTTS-v2 fine-tune cho tiếng Việt (capleaf/viXTTS), clone giọng từ audio mẫu.

Tham số sinh lấy theo demo chính thức của tác giả (github.com/thinhlpg/vixtts-demo).
"""

import re

import numpy as np
import torch
from huggingface_hub import snapshot_download
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.layers.xtts import tokenizer as xtts_tokenizer
from TTS.tts.models.xtts import Xtts

REPO = "capleaf/viXTTS"
REFERENCE = "samples/nu-luu-loat.wav"  # giọng nữ mẫu đi kèm model

# coqui-tts chưa biết "vi": văn bản đầu vào đã được chuẩn hóa sẵn nên chỉ cần hạ chữ thường.
_orig_preprocess = xtts_tokenizer.VoiceBpeTokenizer.preprocess_text


def _preprocess(self, txt, lang):
    if lang == "vi":
        return re.sub(r"\s+", " ", txt.lower()).strip()
    return _orig_preprocess(self, txt, lang)


xtts_tokenizer.VoiceBpeTokenizer.preprocess_text = _preprocess


class Engine:
    name = "viXTTS"
    license = "CPML (non-commercial)"
    repo = REPO

    def __init__(self, device: str):
        path = snapshot_download(REPO)
        config = XttsConfig()
        config.load_json(f"{path}/config.json")
        self.model = Xtts.init_from_config(config)
        self.model.load_checkpoint(config, checkpoint_dir=path, vocab_path=f"{path}/vocab.json", use_deepspeed=False)
        self.model.to(device).eval()
        self.sample_rate = config.audio.output_sample_rate
        self.gpt_latent, self.speaker_emb = self.model.get_conditioning_latents(audio_path=[f"{path}/{REFERENCE}"])

    @torch.inference_mode()
    def synth(self, text: str, seed: int) -> np.ndarray:
        torch.manual_seed(seed)
        out = self.model.inference(
            text,
            "vi",
            self.gpt_latent,
            self.speaker_emb,
            temperature=0.3,
            length_penalty=1.0,
            repetition_penalty=10.0,
            top_k=30,
            top_p=0.85,
            enable_text_splitting=False,
        )
        return np.asarray(out["wav"], dtype=np.float32)
