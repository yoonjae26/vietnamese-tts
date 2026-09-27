"""Adapter cho từng model TTS.

Mỗi module định nghĩa `class Engine` với:
    name: str
    license: str
    sample_rate: int
    __init__(self, device: str)
    synth(self, text: str, seed: int) -> np.ndarray   # float32 mono

Các model có thư viện xung đột nhau, nên mỗi adapter chạy trong môi trường conda
riêng (xem cột `env` trong ENGINES). Driver `synthesize.py` import adapter theo tên.
"""

ENGINES = {
    # tên: (module, môi trường conda)
    "mms": ("engines.mms", "vitts-coqui"),
    "vixtts": ("engines.vixtts", "vitts-coqui"),
    "f5": ("engines.f5", "vitts-f5"),
    "vieneu": ("engines.vieneu", "vitts-vieneu"),
    "viettts": ("engines.viettts", "vitts-viettts"),
    "indextts2": ("engines.indextts2", "vitts-indextts"),
    "piper": ("engines.piper", "vitts-coqui"),  # chạy với --cpu
}
