"""Đánh giá LLM qua OpenAI API cho việc phiên âm từ nước ngoài, trên cùng bộ test và cách chấm.

    python training/translit/api_baseline.py --list-models --env-file ~/path/.env
    python training/translit/api_baseline.py --model gpt-4.1-mini --env-file ~/path/.env

- Gộp 50 từ mỗi request, model trả về JSON {từ: cách đọc}.
- zero-shot và few-shot (20 ví dụ cố định từ phần train, giống llm_baseline.py).
- Kết quả được lưu đệm ở outputs/api_cache/, chạy lại không tốn thêm token.
- Khóa API đọc từ biến OPENAI_API_KEY hoặc từ --env-file; không bao giờ in ra hay ghi vào file.
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).parent))

from llm_baseline import SYSTEM, clean, few_shot_examples  # noqa: E402
from train import read  # noqa: E402

CACHE = ROOT / "outputs" / "api_cache"
BATCH = 50


def load_key(env_file: str | None) -> str:
    if os.environ.get("OPENAI_API_KEY"):
        return os.environ["OPENAI_API_KEY"]
    if env_file:
        for line in Path(env_file).expanduser().read_text(encoding="utf-8").splitlines():
            m = re.match(r"^\s*(?:export\s+)?(?:OPENAI_)?API_KEY\s*=\s*(.+?)\s*$", line, re.IGNORECASE)
            if m:
                return m.group(1).strip("\"'")
    sys.exit("Không tìm thấy khóa: đặt OPENAI_API_KEY hoặc truyền --env-file có dòng api_key=...")


def batch_prompt(words: list[str], shots: list[tuple[str, str]]) -> list[dict]:
    instructions = SYSTEM + (
        " Bạn sẽ nhận một danh sách từ. Trả về duy nhất một đối tượng JSON, mỗi khóa là một từ trong danh sách "
        "(giữ nguyên chữ thường), giá trị là cách đọc tiếng Việt."
    )
    if shots:
        instructions += " Ví dụ: " + json.dumps(dict(shots), ensure_ascii=False)
    return [
        {"role": "system", "content": instructions},
        {"role": "user", "content": json.dumps(words, ensure_ascii=False)},
    ]


def run(client, model: str, words: list[str], shots, tag: str) -> tuple[dict[str, str], dict]:
    CACHE.mkdir(parents=True, exist_ok=True)
    cache_file = CACHE / f"{model.replace('/', '_')}_{tag}.json"
    cache = json.loads(cache_file.read_text(encoding="utf-8")) if cache_file.exists() else {"out": {}, "usage": {}}
    todo = [w for w in words if w not in cache["out"]]
    usage = cache["usage"] or {"input": 0, "output": 0, "requests": 0}
    for i in range(0, len(todo), BATCH):
        chunk = todo[i : i + BATCH]
        for attempt in range(3):
            try:
                resp = client.chat.completions.create(
                    model=model,
                    messages=batch_prompt(chunk, shots),
                    response_format={"type": "json_object"},
                    temperature=0,
                )
                data = json.loads(resp.choices[0].message.content)
                break
            except Exception as e:  # lỗi mạng / JSON hỏng: thử lại, không in khóa
                print(f"  lỗi request ({type(e).__name__}), thử lại {attempt + 1}/3", flush=True)
                time.sleep(2 * (attempt + 1))
        else:
            data = {}
        usage["input"] += resp.usage.prompt_tokens if data else 0
        usage["output"] += resp.usage.completion_tokens if data else 0
        usage["requests"] += 1
        lowered = {str(k).lower(): str(v) for k, v in data.items()}
        for w in chunk:
            cache["out"][w] = clean(lowered.get(w, ""))
        cache["usage"] = usage
        cache_file.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")
        print(
            f"  {tag}: {min(i + BATCH, len(todo))}/{len(todo)} từ | token vào {usage['input']:,} ra {usage['output']:,}"
        )
    return cache["out"], usage


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="gpt-4.1-mini")
    p.add_argument("--env-file")
    p.add_argument("--list-models", action="store_true")
    args = p.parse_args()

    from openai import OpenAI

    client = OpenAI(api_key=load_key(args.env_file))
    if args.list_models:
        ids = sorted(m.id for m in client.models.list().data)
        print("\n".join(i for i in ids if re.match(r"(gpt|o\d|chatgpt)", i)))
        return

    from evaluate import score

    test = read("test")
    words = [w for w, _ in test]
    rows = []
    for tag, shots in (("zero-shot", []), ("few-shot", few_shot_examples(read("train"), k=20))):
        t0 = time.perf_counter()
        preds, usage = run(client, args.model, words, shots, tag)
        scores = [score(preds.get(w, ""), refs) for w, refs in test]
        rows.append(
            {
                "system": f"{args.model} {tag}" + (" (20 ví dụ từ train)" if shots else ""),
                "exact": sum(s["exact"] for s in scores) / len(scores),
                "ser": sum(s["ser"] for s in scores) / len(scores),
                "cer": sum(s["cer"] for s in scores) / len(scores),
                "seconds": time.perf_counter() - t0,
                "usage": usage,
                "missing": sum(1 for w in words if not preds.get(w)),
            }
        )
        r = rows[-1]
        print(
            f"{r['system']}: đúng {r['exact']:.1%} SER {r['ser']:.1%} | "
            f"token vào {usage['input']:,} ra {usage['output']:,}"
        )

    out = ROOT / "results" / f"translit_api_{args.model.replace('/', '_')}.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print("DONE", out)


if __name__ == "__main__":
    main()
