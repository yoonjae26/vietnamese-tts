"""LLM làm đối thủ so sánh cho việc phiên âm từ nước ngoài -> tiếng Việt.

Mặc định Qwen2.5-7B-Instruct, giải mã tham lam (greedy), sinh theo lô trên GPU 0.
- zero-shot: chỉ có hướng dẫn.
- few-shot: thêm K ví dụ cố định lấy ngẫu nhiên (seed cố định) từ phần TRAIN, giống dữ liệu
  mà model vitts được học, để so sánh công bằng.
"""

import random
import re
import unicodedata

import torch

SYSTEM = (
    "Bạn là chuyên gia phiên âm từ nước ngoài sang cách đọc tiếng Việt cho hệ thống chuyển văn bản "
    "thành giọng nói. Với mỗi từ, hãy viết cách người Việt đọc từ đó bằng các âm tiết tiếng Việt có dấu, "
    "viết thường, các âm tiết cách nhau bằng dấu cách. Ví dụ: container -> công tê nơ. "
    "Chỉ trả lời cách đọc, không giải thích."
)
_VIET_CHARS = re.compile(r"[^a-zàáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ ]")


def clean(output: str) -> str:
    """Lấy dòng đầu, bỏ phần '->' lặp lại từ gốc, bỏ ký tự ngoài bảng chữ tiếng Việt."""
    line = unicodedata.normalize("NFC", output.strip().splitlines()[0] if output.strip() else "").lower()
    line = line.split("->")[-1].split(":")[-1]
    line = _VIET_CHARS.sub(" ", line.replace("-", " "))
    return re.sub(r"\s+", " ", line).strip()


class LLMTransliterator:
    def __init__(self, model_id: str, shots: list[tuple[str, str]] | None = None, device: str = "cuda:0"):
        from transformers import AutoModelForCausalLM, AutoTokenizer

        self.model_id = model_id
        self.device = device
        self.tok = AutoTokenizer.from_pretrained(model_id, padding_side="left")
        self.model = AutoModelForCausalLM.from_pretrained(model_id, dtype=torch.bfloat16).to(device).eval()
        self.shots = shots or []
        self.cache: dict[str, str] = {}

    @property
    def params(self) -> int:
        return sum(p.numel() for p in self.model.parameters())

    def _prompt(self, word: str) -> str:
        messages = [{"role": "system", "content": SYSTEM}]
        for w, t in self.shots:
            messages += [{"role": "user", "content": w}, {"role": "assistant", "content": t}]
        messages.append({"role": "user", "content": word})
        return self.tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

    @torch.inference_mode()
    def batch(self, words: list[str], batch_size: int = 64) -> list[str]:
        todo = [w for w in dict.fromkeys(w.lower() for w in words) if w not in self.cache]
        for i in range(0, len(todo), batch_size):
            chunk = todo[i : i + batch_size]
            enc = self.tok([self._prompt(w) for w in chunk], return_tensors="pt", padding=True).to(self.device)
            out = self.model.generate(**enc, max_new_tokens=32, do_sample=False, pad_token_id=self.tok.eos_token_id)
            texts = self.tok.batch_decode(out[:, enc["input_ids"].shape[1] :], skip_special_tokens=True)
            self.cache.update({w: clean(t) for w, t in zip(chunk, texts, strict=True)})
        return [self.cache[w.lower()] for w in words]

    def __call__(self, word: str) -> str:
        return self.batch([word])[0]


def few_shot_examples(train_rows: list[tuple[str, list[str]]], k: int = 20, seed: int = 0) -> list[tuple[str, str]]:
    rng = random.Random(seed)
    return [(w, refs[0]) for w, refs in rng.sample(train_rows, k)]
