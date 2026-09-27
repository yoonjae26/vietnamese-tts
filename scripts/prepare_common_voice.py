"""Chuyển Common Voice tiếng Việt (mp3) sang wav mono 22050 Hz cho formatter `vi_common_voice`.

python scripts/prepare_common_voice.py --root data/cv-corpus-xx/vi --meta validated.tsv
"""

import argparse
import csv
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import librosa
import soundfile as sf


def convert(src: Path, dst: Path, sr: int) -> None:
    if dst.exists():
        return
    wav, _ = librosa.load(src, sr=sr, mono=True)
    wav, _ = librosa.effects.trim(wav, top_db=30)
    sf.write(dst, wav, sr, subtype="PCM_16")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--meta", default="validated.tsv")
    parser.add_argument("--sr", type=int, default=22050)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()

    root = Path(args.root)
    out_dir = root / "clips_wav"
    out_dir.mkdir(exist_ok=True)
    with open(root / args.meta, encoding="utf-8", newline="") as f:
        names = [row["path"] for row in csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)]

    with ProcessPoolExecutor(args.workers) as pool:
        futures = [
            pool.submit(convert, root / "clips" / n, out_dir / Path(n).with_suffix(".wav").name, args.sr) for n in names
        ]
        for i, fut in enumerate(futures, 1):
            fut.result()
            if i % 500 == 0:
                print(f"{i}/{len(names)}")
    print(f"Xong: {len(names)} file -> {out_dir}")


if __name__ == "__main__":
    main()
