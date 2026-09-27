"""Độ tự nhiên (UTMOS) và độ giống giọng (speaker similarity) của audio sinh ra.

- UTMOS22-strong (github.com/tarepan/SpeechMOS): dự đoán MOS 1 đến 5. Model được huấn luyện
  trên tiếng Anh, nên với tiếng Việt chỉ dùng để so sánh tương đối giữa các model.
- SIM: cosine giữa embedding ECAPA-TDNN (`speechbrain/spkrec-ecapa-voxceleb`) của giọng mẫu và của audio
  sinh ra. Tính cho mọi model; với MMS và Piper (giọng cố định, người khác) nó là mốc "khác người nói".
  Đã thử `microsoft/wavlm-base-plus-sv` trước: một giọng nữ khác hẳn (Piper) vẫn đạt 0.94, gần bằng các
  model clone (0.95 đến 0.98), tức là nó gần như chỉ tách được giới tính, nên đã bỏ.

Mọi audio được cắt khoảng lặng đầu/cuối trước khi chấm, để khoảng lặng thừa (lỗi "không dừng")
không làm lệch điểm. Lỗi đó đã được đo riêng.
"""

import librosa
import numpy as np
import soundfile as sf
import torch

SR = 16000
SV_MODEL = "speechbrain/spkrec-ecapa-voxceleb"
UTMOS_HUB = ("tarepan/SpeechMOS:v1.2.0", "utmos22_strong")
CLONING = {"vixtts", "f5", "vieneu", "viettts", "indextts2"}  # model clone từ giọng mẫu


def load_16k(path) -> np.ndarray:
    wav, sr = sf.read(path, dtype="float32")
    if wav.ndim > 1:
        wav = wav.mean(axis=1)
    if sr != SR:
        wav = librosa.resample(wav, orig_sr=sr, target_sr=SR)
    wav, _ = librosa.effects.trim(wav, top_db=40)
    return np.ascontiguousarray(wav)


class Scorers:
    def __init__(self, device: str, reference_wav: str):
        from speechbrain.inference.speaker import EncoderClassifier

        self.device = device
        self.utmos = torch.hub.load(*UTMOS_HUB, trust_repo=True).to(device).eval()
        self.sv = EncoderClassifier.from_hparams(source=SV_MODEL, run_opts={"device": device})
        self.ref_emb = self.embed(load_16k(reference_wav))

    @torch.inference_mode()
    def mos(self, wav: np.ndarray) -> float:
        return float(self.utmos(torch.from_numpy(wav).unsqueeze(0).to(self.device), SR).item())

    @torch.inference_mode()
    def embed(self, wav: np.ndarray) -> torch.Tensor:
        emb = self.sv.encode_batch(torch.from_numpy(wav).unsqueeze(0).to(self.device)).reshape(-1)
        return torch.nn.functional.normalize(emb, dim=-1)

    def similarity(self, wav: np.ndarray) -> float:
        return float((self.embed(wav) @ self.ref_emb).item())
