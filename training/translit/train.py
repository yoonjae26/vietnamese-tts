"""Huấn luyện model phiên âm từ nước ngoài -> tiếng Việt.

    CUDA_VISIBLE_DEVICES=0 python training/translit/train.py
    CUDA_VISIBLE_DEVICES=0 python training/translit/train.py --d-model 384 --layers 4 --epochs 200

Ghi checkpoint tốt nhất theo dev (độ chính xác cả từ) vào models/translit/translit.pt.
"""

import argparse
import json
import math
import os
import random
import sys
import time
from pathlib import Path

import torch
from torch import nn

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from vitts.translit.model import PAD, Config, Seq2Seq, Vocab, save, source_tokens  # noqa: E402

DATA = ROOT / "data" / "translit"


def read(split: str, data_dir: Path = DATA) -> list[tuple[str, list[str]]]:
    rows = []
    for line in (data_dir / f"{split}.tsv").read_text(encoding="utf-8").splitlines():
        word, refs = line.split("\t")
        rows.append((word, refs.split(" | ")))
    return rows


PHONES: dict = {}  # từ -> âm vị CMUdict (chỉ khi --phonemes)
PHONE_DROP = 0.2  # tỉ lệ bỏ âm vị khi huấn luyện, để model vẫn đọc được từ không có trong CMUdict


def src_of(word: str, train: bool) -> list[str]:
    phones = PHONES.get(word)
    if phones and train and random.random() < PHONE_DROP:
        phones = None
    return source_tokens(word, phones)


def batches(pairs, src_vocab, tgt_vocab, size, shuffle, device):
    idx = list(range(len(pairs)))
    if shuffle:
        random.shuffle(idx)
    for i in range(0, len(idx), size):
        chunk = [pairs[j] for j in idx[i : i + size]]
        src = [src_vocab.encode(src_of(w, shuffle)) for w, _ in chunk]
        tgt = [tgt_vocab.encode(t) for _, t in chunk]
        s = torch.full((len(chunk), max(map(len, src))), PAD, dtype=torch.long)
        t = torch.full((len(chunk), max(map(len, tgt))), PAD, dtype=torch.long)
        for k, (a, b) in enumerate(zip(src, tgt, strict=True)):
            s[k, : len(a)], t[k, : len(b)] = torch.tensor(a), torch.tensor(b)
        yield s.to(device), t.to(device)


def accuracy(model, rows, src_vocab, tgt_vocab, device) -> float:
    model.eval()
    correct = 0
    for i in range(0, len(rows), 512):
        chunk = rows[i : i + 512]
        src = [src_vocab.encode(src_of(w, False)) for w, _ in chunk]
        s = torch.full((len(chunk), max(map(len, src))), PAD, dtype=torch.long)
        for k, a in enumerate(src):
            s[k, : len(a)] = torch.tensor(a)
        out = model.greedy(s.to(device))
        for (_, refs), ids in zip(chunk, out.tolist(), strict=True):
            correct += tgt_vocab.decode(ids) in refs
    return correct / len(rows)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--d-model", type=int, default=256)
    p.add_argument("--layers", type=int, default=3)
    p.add_argument("--heads", type=int, default=4)
    p.add_argument("--dropout", type=float, default=0.1)
    p.add_argument("--epochs", type=int, default=150)
    p.add_argument("--batch", type=int, default=256)
    p.add_argument("--lr", type=float, default=7e-4)
    p.add_argument("--warmup", type=int, default=1000)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--phonemes", action="store_true", help="thêm âm vị CMUdict vào đầu vào")
    p.add_argument("--out", default=str(ROOT / "models" / "translit" / "translit.pt"))
    p.add_argument("--data", default="", help="thư mục con của data/translit: '' (từ điển), 'gpt', 'both'")
    args = p.parse_args()

    if os.environ.get("CUDA_VISIBLE_DEVICES") != "0":
        sys.exit("Cần CUDA_VISIBLE_DEVICES=0 (máy dùng chung, chỉ GPU 0).")
    device = "cuda:0"
    random.seed(args.seed)
    torch.manual_seed(args.seed)

    data_dir = DATA / args.data if args.data else DATA
    train, dev = read("train", data_dir), read("dev", data_dir)
    train_pairs = [(w, t) for w, refs in train for t in refs]
    if args.phonemes:
        import cmudict

        d = cmudict.dict()
        PHONES.update({w: d[w][0] for w, _ in train + dev if w in d})
    src_vocab = Vocab([tok for w, _ in train_pairs for tok in source_tokens(w, PHONES.get(w))])
    tgt_vocab = Vocab([c for _, t in train_pairs for c in t])
    cfg = Config(
        d_model=args.d_model,
        nhead=args.heads,
        enc_layers=args.layers,
        dec_layers=args.layers,
        ff=4 * args.d_model,
        dropout=args.dropout,
    )
    model = Seq2Seq(cfg, len(src_vocab), len(tgt_vocab)).to(device)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"train={len(train_pairs)} dev={len(dev)} | src_vocab={len(src_vocab)} tgt_vocab={len(tgt_vocab)} | "
          f"params={n_params / 1e6:.2f}M", flush=True)  # fmt: skip

    opt = torch.optim.AdamW(model.parameters(), lr=args.lr, betas=(0.9, 0.98), weight_decay=0.01)
    steps_total = args.epochs * math.ceil(len(train_pairs) / args.batch)
    sched = torch.optim.lr_scheduler.LambdaLR(
        opt,
        lambda s: min((s + 1) / args.warmup, 0.5 * (1 + math.cos(math.pi * min(s / steps_total, 1.0)))),
    )
    loss_fn = nn.CrossEntropyLoss(ignore_index=PAD, label_smoothing=0.1)

    best, history, t0 = -1.0, [], time.time()
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    for epoch in range(1, args.epochs + 1):
        model.train()
        total, n = 0.0, 0
        for src, tgt in batches(train_pairs, src_vocab, tgt_vocab, args.batch, True, device):
            logits = model(src, tgt[:, :-1])
            loss = loss_fn(logits.reshape(-1, logits.size(-1)), tgt[:, 1:].reshape(-1))
            opt.zero_grad(set_to_none=True)
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
            sched.step()
            total, n = total + loss.item(), n + 1
        if epoch % 5 == 0 or epoch == args.epochs:
            acc = accuracy(model, dev, src_vocab, tgt_vocab, device)
            history.append({"epoch": epoch, "loss": total / n, "dev_acc": acc})
            mark = ""
            if acc > best:
                best, mark = acc, " *"
                save(args.out, model, src_vocab, tgt_vocab, {"dev_acc": acc, "epoch": epoch, "args": vars(args)})
            print(
                f"epoch {epoch:3d} loss {total / n:.3f} dev_acc {acc:.1%}{mark} ({time.time() - t0:.0f}s)", flush=True
            )

    (Path(args.out).parent / "train_history.json").write_text(json.dumps(history, indent=1))
    print(f"DONE best dev_acc {best:.1%} -> {args.out}", flush=True)


if __name__ == "__main__":
    main()
