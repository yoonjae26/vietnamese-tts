"""Transformer seq2seq mức ký tự: từ nước ngoài (chữ Latin) -> cách đọc tiếng Việt (âm tiết có dấu).

"container" -> "công tê nơ"
"""

import math
from dataclasses import asdict, dataclass

import torch
from torch import nn

PAD, BOS, EOS, UNK = 0, 1, 2, 3
SPECIALS = ["<pad>", "<s>", "</s>", "<unk>"]


@dataclass
class Config:
    d_model: int = 256
    nhead: int = 4
    enc_layers: int = 3
    dec_layers: int = 3
    ff: int = 1024
    dropout: float = 0.1
    max_len: int = 64


class Vocab:
    def __init__(self, chars: list[str]):
        self.itos = SPECIALS + sorted(set(chars) - set(SPECIALS))
        self.stoi = {c: i for i, c in enumerate(self.itos)}

    def encode(self, s: str, bos_eos: bool = True) -> list[int]:
        ids = [self.stoi.get(c, UNK) for c in s]
        return [BOS, *ids, EOS] if bos_eos else ids

    def decode(self, ids) -> str:
        out = []
        for i in ids:
            if i == EOS:
                break
            if i >= len(SPECIALS):
                out.append(self.itos[i])
        return "".join(out)

    def __len__(self):
        return len(self.itos)


class Seq2Seq(nn.Module):
    def __init__(self, cfg: Config, src_vocab: int, tgt_vocab: int):
        super().__init__()
        self.cfg = cfg
        self.src_emb = nn.Embedding(src_vocab, cfg.d_model, padding_idx=PAD)
        self.tgt_emb = nn.Embedding(tgt_vocab, cfg.d_model, padding_idx=PAD)
        self.pos = nn.Embedding(cfg.max_len, cfg.d_model)
        self.transformer = nn.Transformer(
            d_model=cfg.d_model,
            nhead=cfg.nhead,
            num_encoder_layers=cfg.enc_layers,
            num_decoder_layers=cfg.dec_layers,
            dim_feedforward=cfg.ff,
            dropout=cfg.dropout,
            batch_first=True,
            norm_first=True,
        )
        self.out = nn.Linear(cfg.d_model, tgt_vocab)
        self.scale = math.sqrt(cfg.d_model)

    def _embed(self, emb: nn.Embedding, x: torch.Tensor) -> torch.Tensor:
        pos = torch.arange(x.size(1), device=x.device)
        return emb(x) * self.scale + self.pos(pos)

    def encode(self, src: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        mask = src == PAD
        return self.transformer.encoder(self._embed(self.src_emb, src), src_key_padding_mask=mask), mask

    def decode(self, memory, src_mask, tgt: torch.Tensor) -> torch.Tensor:
        causal = self.transformer.generate_square_subsequent_mask(tgt.size(1), device=tgt.device, dtype=torch.bool)
        h = self.transformer.decoder(
            self._embed(self.tgt_emb, tgt),
            memory,
            tgt_mask=causal,
            tgt_key_padding_mask=tgt == PAD,
            memory_key_padding_mask=src_mask,
        )
        return self.out(h)

    def forward(self, src, tgt_in):
        memory, src_mask = self.encode(src)
        return self.decode(memory, src_mask, tgt_in)

    @torch.inference_mode()
    def greedy(self, src: torch.Tensor, max_len: int = 48) -> torch.Tensor:
        memory, src_mask = self.encode(src)
        ys = torch.full((src.size(0), 1), BOS, dtype=torch.long, device=src.device)
        done = torch.zeros(src.size(0), dtype=torch.bool, device=src.device)
        for _ in range(max_len):
            nxt = self.decode(memory, src_mask, ys)[:, -1].argmax(-1)
            nxt = torch.where(done, torch.full_like(nxt, PAD), nxt)
            ys = torch.cat([ys, nxt[:, None]], dim=1)
            done |= nxt == EOS
            if done.all():
                break
        return ys[:, 1:]

    @torch.inference_mode()
    def beam(self, src: torch.Tensor, width: int = 5, max_len: int = 48) -> list[int]:
        """Beam search cho một từ (src: [1, T]). Điểm chuẩn hóa theo độ dài."""
        memory, src_mask = self.encode(src)
        beams = [([BOS], 0.0, False)]
        for _ in range(max_len):
            alive = [b for b in beams if not b[2]]
            if not alive:
                break
            ys = torch.tensor([b[0] for b in alive], device=src.device)
            logp = self.decode(memory.expand(len(alive), -1, -1), src_mask.expand(len(alive), -1), ys)[:, -1]
            logp = logp.log_softmax(-1)
            cand = [b for b in beams if b[2]]
            top = logp.topk(width, dim=-1)
            for k, (seq, score, _) in enumerate(alive):
                for lp, idx in zip(top.values[k].tolist(), top.indices[k].tolist(), strict=True):
                    cand.append((seq + [idx], score + lp, idx == EOS))
            beams = sorted(cand, key=lambda b: b[1] / len(b[0]), reverse=True)[:width]
        return beams[0][0][1:]


def save(path, model: Seq2Seq, src_vocab: Vocab, tgt_vocab: Vocab, extra: dict | None = None):
    torch.save(
        {
            "config": asdict(model.cfg),
            "src_vocab": src_vocab.itos,
            "tgt_vocab": tgt_vocab.itos,
            "state_dict": {k: v.half() if v.is_floating_point() else v for k, v in model.state_dict().items()},
            **(extra or {}),
        },
        path,
    )


def load(path, device: str = "cpu") -> tuple[Seq2Seq, Vocab, Vocab]:
    ckpt = torch.load(path, map_location=device, weights_only=True)
    src_vocab, tgt_vocab = Vocab([]), Vocab([])
    src_vocab.itos, tgt_vocab.itos = ckpt["src_vocab"], ckpt["tgt_vocab"]
    src_vocab.stoi = {c: i for i, c in enumerate(src_vocab.itos)}
    tgt_vocab.stoi = {c: i for i, c in enumerate(tgt_vocab.itos)}
    model = Seq2Seq(Config(**ckpt["config"]), len(src_vocab), len(tgt_vocab))
    model.load_state_dict({k: v.float() if v.is_floating_point() else v for k, v in ckpt["state_dict"].items()})
    return model.to(device).eval(), src_vocab, tgt_vocab
