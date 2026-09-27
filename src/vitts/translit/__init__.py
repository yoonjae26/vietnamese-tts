"""Phiên âm từ nước ngoài sang cách đọc tiếng Việt bằng model đã huấn luyện (cần torch).

from vitts.translit import Transliterator
t = Transliterator.from_pretrained()          # models/translit/translit.pt
t("container")  # 'công tê nơ'
"""

from functools import lru_cache
from pathlib import Path

DEFAULT_CHECKPOINT = Path(__file__).resolve().parents[3] / "models" / "translit" / "translit.pt"


class Transliterator:
    def __init__(self, model, src_vocab, tgt_vocab, device: str = "cpu", beam: int = 5):
        self.model, self.src_vocab, self.tgt_vocab = model, src_vocab, tgt_vocab
        self.device, self.beam_width = device, beam
        self._cached = lru_cache(maxsize=50_000)(self._translit)

    @classmethod
    def from_pretrained(cls, path: str | Path = DEFAULT_CHECKPOINT, device: str = "cpu", beam: int = 5):
        from vitts.translit.model import load

        return cls(*load(path, device), device=device, beam=beam)

    def _translit(self, word: str) -> str:
        import torch

        src = torch.tensor([self.src_vocab.encode(word.lower())], device=self.device)
        if self.beam_width > 1:
            ids = self.model.beam(src, width=self.beam_width)
        else:
            ids = self.model.greedy(src)[0].tolist()
        return self.tgt_vocab.decode(ids)

    def __call__(self, word: str) -> str:
        return self._cached(word.lower())
