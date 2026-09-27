# 🇻🇳 Vietnamese TTS

[![CI](https://github.com/yoonjae26/vietnamese-tts/actions/workflows/ci.yml/badge.svg)](https://github.com/yoonjae26/vietnamese-tts/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)

Bộ công cụ **chuyển văn bản tiếng Việt thành giọng nói**, xây dựng trên [coqui-tts](https://github.com/idiap/coqui-ai-TTS).

coqui-tts hỗ trợ hàng trăm ngôn ngữ nhưng **chưa có xử lý riêng cho tiếng Việt**: XTTS không hỗ trợ `vi`, không có bộ chuẩn hóa văn bản, không có formatter dataset. Dự án này bổ sung những phần còn thiếu đó:

| Thành phần | Mô tả |
| --- | --- |
| 🔤 **Chuẩn hóa văn bản** | Đọc số, ngày tháng, giờ, tiền tệ, đơn vị đo, số điện thoại, chữ viết tắt; thống nhất Unicode và vị trí dấu thanh |
| 🗂️ **Formatter dataset** | Dùng trực tiếp với `load_tts_samples` của coqui: kiểu LJSpeech, cặp wav/txt, Common Voice |
| 🏋️ **Recipe huấn luyện** | Huấn luyện / fine-tune VITS tiếng Việt với bảng ký tự tiếng Việt đầy đủ |
| 🌐 **API server** | FastAPI, **tương thích OpenAI** `/v1/audio/speech`: đổi `base_url` là dùng được |
| 🎛️ **Demo Gradio** | Giao diện web, triển khai được lên Hugging Face Spaces |
| 🐳 **Docker** | Đóng gói server chạy trên CPU |

## Chuẩn hóa văn bản

Model TTS chỉ nhìn thấy ký tự, nên `"100k"` hay `"14h30"` phải được đổi thành chữ trước khi đọc.

```python
from vitts import normalize_text

normalize_text("Giá 100k, giao lúc 14h30 ngày 2/9/2024 tại TP.HCM!")
# 'giá một trăm nghìn, giao lúc mười bốn giờ ba mươi phút ngày hai tháng chín
#  năm hai nghìn không trăm hai mươi tư tại thành phố hồ chí minh!'
```

| Đầu vào | Đầu ra |
| --- | --- |
| `21`, `105`, `1005` | hai mươi mốt, một trăm linh năm, một nghìn không trăm linh năm |
| `1.250.000đ`, `$5`, `100k` | một triệu hai trăm năm mươi nghìn đồng, năm đô la, một trăm nghìn |
| `36,5°C`, `12%`, `60km/h` | ba mươi sáu phẩy năm độ xê, mười hai phần trăm, sáu mươi ki lô mét trên giờ |
| `2/9/2024`, `tháng 4/2023`, `thứ 4` | ngày hai tháng chín năm …, tháng tư năm …, thứ tư |
| `14h30`, `8:05` | mười bốn giờ ba mươi phút, tám giờ năm phút |
| `5-10 người`, `thắng 3-1` | năm đến mười người, thắng ba một |
| `0912 345 678` | không chín một hai ba bốn năm sáu bảy tám |
| `UBND`, `THPT`, `AI`, `U23` | ủy ban nhân dân, trung học phổ thông, a i, u hai mươi ba |
| `hoà`, `thuỷ`, `khoẻ` | hòa, thủy, khỏe (thống nhất vị trí dấu thanh) |

Phần chuẩn hóa **không cần thư viện ngoài**, dùng được cho mọi hệ TTS khác (Piper, F5-TTS, VITS, …).

## Cài đặt

```bash
git clone https://github.com/yoonjae26/vietnamese-tts.git
cd vietnamese-tts
pip install -e ".[server,demo]"     # hoặc chỉ `pip install -e .` nếu chỉ cần chuẩn hóa văn bản
```

## Sử dụng

### Python

```python
from vitts.synthesizer import VietnameseTTS

tts = VietnameseTTS()  # mặc định dùng Meta MMS tiếng Việt (tts_models/vie/fairseq/vits)
audio = tts.synthesize("Xin chào Việt Nam! Hôm nay là ngày 2/9.")
open("out.wav", "wb").write(audio.to_wav_bytes())

# Dùng checkpoint tự huấn luyện
tts = VietnameseTTS(model_path="runs/.../best_model.pth", config_path="runs/.../config.json")
```

Văn bản dài được tự động tách câu, đọc từng đoạn rồi ghép lại.

### API server (tương thích OpenAI)

```bash
vitts-server --port 8000
```

```bash
curl http://localhost:8000/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"input": "Xin chào, tôi là trợ lý giọng nói.", "response_format": "wav"}' \
  -o out.wav
```

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="none")
client.audio.speech.create(model="vitts", voice="default", input="Xin chào!").write_to_file("out.wav")
```

| Endpoint | Mô tả |
| --- | --- |
| `POST /v1/audio/speech` | `input`, `voice`, `speed` (0.25–4), `response_format` (`wav` / `flac` / `pcm`) |
| `POST /v1/normalize` | Trả về văn bản sau chuẩn hóa, tiện để debug |
| `GET /v1/models`, `GET /health` | Thông tin model |

Tài liệu tương tác: `http://localhost:8000/docs`.

### Demo web

```bash
python app.py
```

### Docker

```bash
docker build -t vietnamese-tts .
docker run -p 8000:8000 vietnamese-tts
```

## Huấn luyện model của riêng bạn

1. Chuẩn bị dữ liệu (mono, 22050 Hz):

   ```
   data/my_dataset/
   ├── metadata.csv        # <id>|<văn bản>[|<người nói>]
   └── wavs/<id>.wav
   ```

   Các formatter có sẵn trong [`vitts/datasets.py`](src/vitts/datasets.py):

   | Formatter | Định dạng |
   | --- | --- |
   | `vi_ljspeech` | `metadata.csv` + `wavs/` |
   | `vi_wav_txt_pairs` | Thư mục các cặp `x.wav` + `x.txt`; thư mục con là tên người nói |
   | `vi_common_voice` | Mozilla Common Voice (chạy `scripts/prepare_common_voice.py` để đổi mp3 → wav) |

2. Huấn luyện:

   ```bash
   pip install -e ".[tts]"
   python recipes/vits/train_vits.py --data data/my_dataset --output runs
   tensorboard --logdir runs
   ```

3. Phục vụ model vừa train:

   ```bash
   vitts-server --model-path runs/<run>/best_model.pth --config-path runs/<run>/config.json
   ```

## Cấu trúc dự án

```
src/vitts/
├── text/
│   ├── numbers.py       # đọc số thành chữ
│   ├── normalizer.py    # pipeline chuẩn hóa + tách câu
│   └── symbols.py       # bảng ký tự tiếng Việt cho tokenizer
├── datasets.py          # formatter dataset cho coqui-tts
├── synthesizer.py       # bọc TTS API: chuẩn hóa → tách câu → ghép audio
└── server.py            # FastAPI, tương thích OpenAI
recipes/vits/            # script huấn luyện
app.py                   # demo Gradio
tests/                   # pytest
```

## Phát triển

```bash
pip install -e ".[dev]"
pytest          # unit test + doctest
ruff check . && ruff format --check .
```

## Lộ trình

- [ ] Phát hành checkpoint VITS tiếng Việt lên Hugging Face Hub
- [ ] Demo trên Hugging Face Spaces
- [ ] Streaming audio qua WebSocket
- [ ] Fine-tune XTTS v2 cho tiếng Việt (voice cloning)
- [ ] Hỗ trợ giọng miền Bắc / Trung / Nam
- [ ] Export ONNX để chạy nhanh trên CPU

## Giấy phép

- Mã nguồn dự án: [MIT](LICENSE).
- [coqui-tts](https://github.com/idiap/coqui-ai-TTS): MPL-2.0.
- Model mặc định **Meta MMS** (`tts_models/vie/fairseq/vits`): [CC-BY-NC 4.0](https://github.com/facebookresearch/fairseq/tree/main/examples/mms), **không dùng cho mục đích thương mại**. Hãy tự huấn luyện model nếu cần dùng thương mại.

---

*English:* Vietnamese TTS toolkit on top of coqui-tts: rule-based Vietnamese text normalization (numbers, dates, currency, units, abbreviations, tone-mark placement), dataset formatters, a VITS training recipe, an OpenAI-compatible FastAPI server, and a Gradio demo.
