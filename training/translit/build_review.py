"""Tạo bộ ứng viên để người duyệt chấm "mù" (không biết hệ thống nào tạo ra cách đọc nào).

Lấy ngẫu nhiên 150 từ trong bộ test. Với mỗi từ, gom mọi cách đọc:
- đáp án gốc (từ điển vietnormalizer)
- output của: vitts translit (beam 5), gpt-4o-mini zero/few-shot (từ cache), Qwen2.5-7B few-shot,
  quy tắc của vietnormalizer
- tối đa 3 cách đọc phổ biến do gpt-4o-mini gợi ý
rồi bỏ trùng, xáo trộn. Nguồn của từng ứng viên chỉ lưu ở outputs/review/mapping.json (không đưa
lên trang duyệt).

    CUDA_VISIBLE_DEVICES=0 python training/translit/build_review.py --env-file ~/path/.env
"""

import argparse
import json
import os
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).parent))

from api_baseline import load_key  # noqa: E402
from llm_baseline import clean, few_shot_examples  # noqa: E402
from prepare_data import clean_target  # noqa: E402
from train import read  # noqa: E402

OUT = ROOT / "outputs" / "review"
N_WORDS = 150
SEED = 2026


def gpt_alternatives(client, words: list[str]) -> dict[str, list[str]]:
    cache_file = OUT / "gpt_alternatives.json"
    cache = json.loads(cache_file.read_text(encoding="utf-8")) if cache_file.exists() else {}
    todo = [w for w in words if w not in cache]
    for i in range(0, len(todo), 50):
        chunk = todo[i : i + 50]
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": "Với mỗi từ nước ngoài, liệt kê tối đa 3 cách người Việt thường đọc từ đó, viết bằng âm "
                    "tiết tiếng Việt có dấu, chữ thường, các âm tiết cách nhau bằng dấu cách. Trả về duy nhất JSON "
                    "dạng {từ: [cách đọc, ...]}, khóa là từ gốc viết thường.",
                },
                {"role": "user", "content": json.dumps(chunk, ensure_ascii=False)},
            ],
        )
        data = {str(k).lower(): v for k, v in json.loads(resp.choices[0].message.content).items()}
        for w in chunk:
            vals = data.get(w, [])
            cache[w] = [clean(v) for v in (vals if isinstance(vals, list) else [vals]) if isinstance(v, str)][:3]
        cache_file.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"gợi ý GPT: {min(i + 50, len(todo))}/{len(todo)} | token vào {resp.usage.prompt_tokens} ra "
              f"{resp.usage.completion_tokens}", flush=True)  # fmt: skip
    return cache


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--env-file")
    args = p.parse_args()
    if os.environ.get("CUDA_VISIBLE_DEVICES") != "0":
        sys.exit("Cần CUDA_VISIBLE_DEVICES=0 (máy dùng chung, chỉ GPU 0).")
    OUT.mkdir(parents=True, exist_ok=True)

    test = read("test")
    sample = random.Random(SEED).sample(test, N_WORDS)
    words = [w for w, _ in sample]
    sources: dict[str, dict[str, str]] = {w: {} for w in words}

    for w, refs in sample:
        sources[w]["gold"] = refs[0]

    from vietnormalizer.transliterator import transliterate_word

    for w in words:
        sources[w]["vietnormalizer_rules"] = transliterate_word(w)

    for tag in ("zero-shot", "few-shot"):
        cached = json.loads((ROOT / "outputs" / "api_cache" / f"gpt-4o-mini_{tag}.json").read_text(encoding="utf-8"))
        for w in words:
            sources[w][f"gpt-4o-mini_{tag}"] = cached["out"].get(w, "")

    import torch

    from vitts.translit import Transliterator

    vitts = Transliterator.from_pretrained(device="cuda:0", beam=5)
    for w in words:
        sources[w]["vitts"] = vitts(w)
    del vitts
    torch.cuda.empty_cache()

    from llm_baseline import LLMTransliterator

    qwen = LLMTransliterator("Qwen/Qwen2.5-7B-Instruct", shots=few_shot_examples(read("train"), k=20))
    for w, t in zip(words, qwen.batch(words), strict=True):
        sources[w]["qwen2.5-7b_few-shot"] = t
    del qwen
    torch.cuda.empty_cache()

    from openai import OpenAI

    alts = gpt_alternatives(OpenAI(api_key=load_key(args.env_file)), words)

    rng = random.Random(SEED + 1)
    items, mapping = [], {}
    for k, w in enumerate(words):
        by_text: dict[str, list[str]] = {}
        for src, text in list(sources[w].items()) + [(f"gpt_alt_{i}", t) for i, t in enumerate(alts.get(w, []))]:
            text = clean_target(text)
            if text:
                by_text.setdefault(text, []).append(src)
        texts = list(by_text)
        rng.shuffle(texts)
        cands = [{"id": f"c{i}", "text": t} for i, t in enumerate(texts)]
        items.append({"id": f"w{k:03d}", "word": w, "order": k, "candidates": cands})
        mapping[f"w{k:03d}"] = {"word": w, "candidates": {c["id"]: by_text[c["text"]] for c in cands}}

    (OUT / "items.json").write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT / "mapping.json").write_text(json.dumps(mapping, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT / "predictions.json").write_text(json.dumps(sources, ensure_ascii=False, indent=1), encoding="utf-8")
    n = sum(len(i["candidates"]) for i in items)
    print(f"DONE {len(items)} từ, {n} ứng viên (trung bình {n / len(items):.1f}/từ) -> {OUT}")


if __name__ == "__main__":
    main()
