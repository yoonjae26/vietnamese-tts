"""Tạo dữ liệu cho trang nghe thử `docs/listen/index.html` (GitHub Pages).

Đọc kết quả benchmark (results/tts.json, outputs/tts/*) rồi ghi:
    docs/listen/data.js            # window.BENCH = {...}
    docs/listen/audio/<engine>/<id>.mp3
    docs/listen/index.html         # page.html bọc thành trang HTML đầy đủ

    python docs/listen/build.py
"""

import json
from pathlib import Path

import librosa
import soundfile as sf

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUTPUTS = ROOT / "outputs" / "tts"

# Câu tiêu biểu: mỗi câu cho thấy một điểm mạnh/yếu cụ thể trong kết quả
SAMPLES = [
    ("short-06", "viXTTS đọc bịa thêm từ ở câu ngắn"),
    ("short-09", "IndexTTS-2 không dừng, sinh thêm khoảng lặng dài"),
    ("medium-01", "Câu thường, có địa danh"),
    ("medium-06", "Câu có số đã được đọc thành chữ"),
    ("long-01", "Câu dài: bản tin thời tiết"),
    ("tones-05", "Líu lưỡi: vần khó khuya, khoắt, khuỷu"),
    ("tones-07", "Líu lưỡi: ngoằn ngoèo, nghoe nguẩy"),
    ("names-02", "Địa danh Tây Nguyên, có từ mượn Pleiku"),
]


def run_dir(engine: str) -> Path:
    return OUTPUTS / ("piper-cpu" if engine == "piper" else engine)


def to_mp3(src: Path, dst: Path) -> float:
    wav, sr = sf.read(src, dtype="float32")
    if sr not in (16000, 22050, 24000, 32000, 44100, 48000):
        wav, sr = librosa.resample(wav, orig_sr=sr, target_sr=24000), 24000
    dst.parent.mkdir(parents=True, exist_ok=True)
    sf.write(dst, wav, sr, format="MP3", subtype="MPEG_LAYER_III")
    return len(wav) / sr


def write_index() -> None:
    """page.html là phần nội dung (title, style, body). GitHub Pages cần một tài liệu HTML đầy đủ."""
    page = (HERE / "page.html").read_text(encoding="utf-8")
    head, body = page.split('<div class="wrap">', 1)
    html = (
        '<!doctype html>\n<html lang="vi">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        f"{head.strip()}\n<style>body{{margin:0}}</style>\n</head>\n<body>\n"
        f'<div class="wrap">{body}</body>\n</html>\n'
    )
    (HERE / "index.html").write_text(html, encoding="utf-8")


def main():
    bench = json.loads((ROOT / "results" / "tts.json").read_text(encoding="utf-8"))
    engines = sorted(bench["engines"], key=lambda r: r["overall"]["wer"])
    sentences = {
        s["id"]: s
        for s in map(json.loads, (ROOT / "benchmark/tts/sentences.jsonl").read_text(encoding="utf-8").splitlines())
    }

    ref_src = ROOT / "outputs" / "reference" / "ref_8s.wav"
    ref_seconds = to_mp3(ref_src, HERE / "audio" / "reference.mp3")

    out_engines = []
    for r in engines:
        d = run_dir(r["engine"])
        quality = json.loads((d / "quality.json").read_text(encoding="utf-8"))
        rows = {x["id"]: x for x in r["rows"]}
        clips = {}
        for sid, _ in SAMPLES:
            seconds = to_mp3(d / f"{sid}.wav", HERE / "audio" / r["engine"] / f"{sid}.mp3")
            clips[sid] = {
                "src": f"audio/{r['engine']}/{sid}.mp3",
                "seconds": round(seconds, 2),
                "asr": rows[sid]["hyp"],
                "wer": rows[sid]["wer"],
                "utmos": quality[sid]["utmos"],
                "sim": quality[sid]["sim"],
                "runaway": sid in r["runaway"],
            }
        out_engines.append(
            {
                "id": r["engine"],
                "name": r["name"],
                "repo": r["repo"],
                "license": r["license"],
                "wer": r["overall"]["wer"],
                "utmos": r["utmos"],
                "sim": r["sim"],
                "rtf": r["rtf"],
                "vram": r["peak_vram_gb"],
                "sample_rate": r["sample_rate"],
                "runaway": len(r["runaway"]),
                "clones_voice": r["clones_voice"],
                "n": r["overall"]["n"],
                "clips": clips,
            }
        )

    data = {
        "reference": {"src": "audio/reference.mp3", "seconds": round(ref_seconds, 2), **bench["reference"]},
        "samples": [{"id": sid, "note": note, **sentences[sid]} for sid, note in SAMPLES],
        "engines": out_engines,
    }
    (HERE / "data.js").write_text(
        "window.BENCH = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8"
    )
    write_index()
    size = sum(p.stat().st_size for p in (HERE / "audio").rglob("*.mp3"))
    print(f"{len(out_engines)} model × {len(SAMPLES)} câu, audio {size / 1e6:.1f} MB -> {HERE}")


if __name__ == "__main__":
    main()
