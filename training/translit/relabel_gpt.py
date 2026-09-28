"""Gắn nhãn lại phần train/dev bằng cách đọc của gpt-4o-mini (few-shot 20 ví dụ).

Người duyệt mù chấp nhận cách đọc kiểu GPT thường hơn đáp án của từ điển vietnormalizer
(xem results/translit_reviewed.md), nên thử dùng GPT làm "giáo viên" cho model nhỏ.
Phần test KHÔNG bị gắn nhãn lại: 150 từ đã duyệt nằm trong đó và chỉ dùng để đánh giá.

Ghi ra:
    data/translit/gpt/{train,dev}.tsv     # nhãn GPT
    data/translit/both/{train,dev}.tsv    # từ điển | GPT (hai đáp án cho mỗi từ)
    data/translit/{gpt,both}/test.tsv     # bản sao test gốc (nhãn từ điển), không đổi

    python training/translit/relabel_gpt.py --env-file ~/path/.env
"""

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).parent))

from api_baseline import load_key, run  # noqa: E402
from llm_baseline import few_shot_examples  # noqa: E402
from prepare_data import clean_target  # noqa: E402
from train import read  # noqa: E402

DATA = ROOT / "data" / "translit"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--env-file")
    p.add_argument("--model", default="gpt-4o-mini")
    args = p.parse_args()

    from openai import OpenAI

    client = OpenAI(api_key=load_key(args.env_file))
    train = read("train")
    shots = few_shot_examples(train, k=20)  # giống hệt lúc đánh giá gpt-4o-mini few-shot
    splits = {"train": train, "dev": read("dev")}
    words = [w for rows in splits.values() for w, _ in rows]
    labels, usage = run(client, args.model, words, shots, "few-shot")
    print(f"token: vào {usage['input']:,} ra {usage['output']:,} | {usage['requests']} request")

    for variant in ("gpt", "both"):
        (DATA / variant).mkdir(exist_ok=True)
        shutil.copy(DATA / "test.tsv", DATA / variant / "test.tsv")
    empty = 0
    for split, rows in splits.items():
        with (
            open(DATA / "gpt" / f"{split}.tsv", "w", encoding="utf-8") as g,
            open(DATA / "both" / f"{split}.tsv", "w", encoding="utf-8") as b,
        ):
            for w, refs in rows:
                gpt = clean_target(labels.get(w, ""))
                empty += not gpt
                g.write(f"{w}\t{gpt or refs[0]}\n")  # GPT trả rỗng thì giữ nhãn từ điển
                both = list(dict.fromkeys([*refs, gpt] if gpt else refs))
                b.write(f"{w}\t{' | '.join(both)}\n")
    same = sum(clean_target(labels.get(w, "")) in refs for w, refs in train)
    print(f"GPT trả rỗng: {empty} từ | nhãn GPT trùng từ điển: {same / len(train):.1%} số từ train")
    print("DONE")


if __name__ == "__main__":
    main()
