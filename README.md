# 🇻🇳 ViTTS-Bench: Benchmark mở cho Text-to-Speech tiếng Việt

[![CI](https://github.com/yoonjae26/vietnamese-tts/actions/workflows/ci.yml/badge.svg)](https://github.com/yoonjae26/vietnamese-tts/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)

Mảng TTS tiếng Việt mã nguồn mở đã có nhiều lựa chọn: viXTTS, VietTTS, F5-TTS-Vietnamese, VieNeu-TTS, Piper, Meta MMS…
Mỗi dự án tự báo cáo kết quả trên dữ liệu riêng, nên **rất khó biết nên chọn cái nào**.

ViTTS-Bench so sánh chúng **trên cùng một bộ test, cùng một cách chấm, chạy lại được bằng một lệnh**.

| Hạng mục | Trạng thái |
| --- | --- |
| 🔤 Chuẩn hóa văn bản (Vinorm, soe-vinorm, VietNormalizer, vitts) | ✅ Có kết quả |
| 🔊 Model TTS: độ rõ (WER qua ASR), tốc độ (RTF), VRAM, giấy phép | 🚧 2/7 model (MMS, viXTTS) |
| 🌐 API chung tương thích OpenAI cho mọi model | 🚧 Có khung (`vitts-server`) |

## Kết quả: chuẩn hóa văn bản

Model TTS chỉ đọc được chữ, nên `"100k"`, `"14h30"`, `"TP.HCM"` phải được đổi sang cách đọc trước. Nếu bước này sai, model tốt đến đâu cũng đọc sai.

**Bộ held-out**, 59 câu, là con số chính thức. Ô là **tỉ lệ câu đọc đúng hoàn toàn** (WER trong ngoặc):

| Nhóm | n | vitts (repo này) | [vinorm](https://github.com/v-nhandt21/Vinorm) 2.0.7 | [soe-vinorm](https://pypi.org/project/soe-vinorm/) 0.3.2 | [vietnormalizer](https://github.com/nghimestudio/vietnormalizer) 0.2.3 |
|---|---:|---:|---:|---:|---:|
| number | 13 | 62% (11.8%) | 69% (6.6%) | **100% (0.0%)** | 69% (6.6%) |
| date | 5 | **100% (0.0%)** | 80% (2.5%) | **100% (0.0%)** | 60% (5.0%) |
| time | 4 | **100% (0.0%)** | **100% (0.0%)** | **100% (0.0%)** | **100% (0.0%)** |
| unit | 7 | 29% (33.3%) | 43% (24.0%) | **71% (4.0%)** | 14% (53.3%) |
| currency | 5 | **80% (9.4%)** | 40% (18.8%) | 40% (25.0%) | 60% (18.8%) |
| percent | 1 | **100% (0.0%)** | 0% (37.5%) | **100% (0.0%)** | 0% (12.5%) |
| phone | 3 | **67% (7.4%)** | **67% (7.4%)** | **67% (7.4%)** | 0% (67.9%) |
| abbreviation | 6 | 17% (43.8%) | **83% (6.2%)** | **83% (6.2%)** | 0% (62.5%) |
| acronym | 3 | **33% (42.9%)** | 0% (46.2%) | 0% (46.2%) | **33% (38.5%)** |
| foreign | 3 | 0% (57.9%) | 0% (41.2%) | 0% (35.3%) | **33% (52.6%)** |
| plain | 4 | **100% (0.0%)** | **100% (0.0%)** | **100% (0.0%)** | **100% (0.0%)** |
| mixed | 5 | 60% (7.4%) | 40% (12.6%) | **80% (6.3%)** | 0% (20.0%) |
| **Tổng** | **59** | 59% (15.3%) | 59% (12.7%) | **76% (7.2%)** | 44% (25.3%) |
| ms / câu | | 0.1 | 30.6 | 0.3 | 0.2 |

**Nhận xét**
- **soe-vinorm tốt nhất tổng thể** (76%), mạnh ở số, đơn vị và viết tắt.
- Chưa bộ nào xử lý tốt **từ nước ngoài** (iPhone, SEA Games, IELTS) và **chữ viết tắt đánh vần** (ATM, NATO). Đây là khoảng trống lớn nhất.
- Tiền tệ viết tắt (`50k`, `99.000đ`, `VND/USD`) là điểm yếu chung. vinorm và soe-vinorm đọc `100k` thành "một trăm ca".
- vitts (bản của repo này) mạnh về tiền tệ, ngày giờ, điện thoại, nhưng **yếu ở số La Mã, đơn vị dính số (`1m75`, `1.500W`) và viết tắt địa danh (`Q.1`, `P.`)**.

Kết quả chi tiết từng câu: [`results/normalization_heldout_errors.md`](results/normalization_heldout_errors.md).

### Phương pháp, và vì sao có hai bộ test

| Bộ | Số câu | Vai trò |
| --- | ---: | --- |
| `dev` | 99 | Dùng trong lúc phát triển vitts. **vitts đã được sửa dựa trên bộ này**, nên điểm của nó ở đây (100%) không phản ánh năng lực thật. |
| `heldout` | 59 | Viết sau khi vitts đã xong, gồm các hiện tượng chưa được code riêng. **Không sửa vitts dựa trên bộ này.** Đây là con số công bố. |

- Đáp án được **viết tay** theo cách đọc tự nhiên, không sinh từ output của bộ chuẩn hóa nào. Một câu có thể có nhiều đáp án đúng, ví dụ "đồng **một** lít", "đồng **mỗi** lít", "đồng **trên** lít".
- Trước khi so sánh, bỏ dấu câu và hoa/thường, rồi quy các biến thể vùng miền về một dạng: *ngàn/nghìn, lẻ/linh, tỉ/tỷ, mươi bốn/mươi tư, kí lô/ki lô, tháng bốn/tháng tư, Việt Nam đồng/đồng…* ([`metrics.py`](src/vitts/bench/metrics.py)).
- **Hạn chế:** bộ test do một người viết và còn nhỏ. Hãy đóng góp thêm câu, nhất là câu từ nguồn thực tế (báo, mạng xã hội, văn bản hành chính). Khi vitts được cải thiện, phiên bản mới phải được đo trên một bộ held-out mới.

### Chạy lại

```bash
pip install -e ".[bench]"
python benchmark/normalization/build_testset.py
python benchmark/normalization/run.py --split heldout
python benchmark/normalization/run.py --split dev
```

## Kết quả: model TTS (đang cập nhật)

50 câu chung, đã ở dạng đọc (không số, không viết tắt), nên chỉ đo chất lượng model. ASR [`vinai/PhoWhisper-large`](https://huggingface.co/vinai/PhoWhisper-large) nghe lại audio, rồi tính WER so với câu gốc. Mỗi model dùng tham số do tác giả khuyến nghị và seed cố định.

| Model | WER ↓ | CER ↓ | WER câu ngắn | WER câu dài | WER thanh điệu khó | RTF ↓ (H200) | VRAM | Giấy phép |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| [MMS-TTS (Meta)](https://huggingface.co/facebook/mms-tts-vie) | **6.9%** | 3.4% | 11.1% | 3.5% | 28.4% | 0.013 | 0.4 GB | CC-BY-NC-4.0 |
| [viXTTS](https://huggingface.co/capleaf/viXTTS) | 9.8% | 5.9% | 55.6% | **2.2%** | 43.2% | 0.203 | 2.2 GB | CPML |

- **viXTTS rất rõ ở câu dài nhưng "bịa" từ ở câu ngắn**: "chúc mừng năm mới" bị đọc thành "chúc mừng năm nợ yết hôn thây". Kết quả này khớp với hạn chế tác giả tự ghi (câu dưới 10 từ).
- **MMS nhỏ và nhanh** (RTF 0.013, tức nhanh hơn thời gian thực khoảng 75 lần) nhưng chỉ có một giọng, âm thanh 16 kHz.
- Bảng đầy đủ: [`results/tts.md`](results/tts.md). Transcript từng câu: [`results/tts.json`](results/tts.json).
- **Hạn chế:** WER qua ASR đo *độ rõ*, không đo *độ tự nhiên*. Nhóm "thanh điệu khó" gồm các câu líu lưỡi, nên ASR cũng dễ nghe nhầm. Cần thêm bản ghi người đọc thật để biết mức lỗi nền của chính ASR.

```bash
# mỗi model chạy trong môi trường riêng (xem benchmark/tts/engines/__init__.py)
CUDA_VISIBLE_DEVICES=0 python benchmark/tts/synthesize.py --engine vixtts
CUDA_VISIBLE_DEVICES=0 python benchmark/tts/evaluate.py
```

## Lộ trình

**Giai đoạn 2: benchmark model TTS**
- [ ] Bộ câu chung cho mọi model: câu ngắn, câu dài, câu có số, từ mượn, tên riêng
- [ ] Độ rõ: ASR tiếng Việt (PhoWhisper / Whisper) nghe lại audio → WER/CER
- [ ] Tốc độ: RTF trên CPU và GPU, thời gian ra audio đầu tiên, VRAM
- [ ] Độ giống giọng khi clone (speaker similarity), MOS dự đoán (UTMOS)
- [ ] Các model: Meta MMS, viXTTS, VietTTS, F5-TTS-Vietnamese, VieNeu-TTS, Piper VITS
- [ ] Trang nghe thử: cùng một câu, mọi model

**Giai đoạn 3: API chung**
- [ ] Một server tương thích OpenAI, chọn model bằng tham số `model`

**vitts normalizer v0.2**
- [ ] Số dính chữ (`12A`, `1m75`, `1.500W`), số La Mã, phân số, số âm
- [ ] Viết tắt hành chính (`Q.`, `P.`, `GD&ĐT`, `CNTT`), từ điển từ nước ngoài
- [ ] Đo trên bộ held-out mới (`HELDOUT_V2`)

## Thành phần khác trong repo

| Thành phần | Mô tả |
| --- | --- |
| [`vitts.text`](src/vitts/text/) | Bộ chuẩn hóa tiếng Việt, không phụ thuộc thư viện ngoài |
| [`vitts.datasets`](src/vitts/datasets.py) | Formatter dataset cho coqui-tts (LJSpeech, cặp wav/txt, Common Voice) |
| [`recipes/vits`](recipes/vits/) | Script huấn luyện VITS tiếng Việt bằng coqui-tts |
| [`vitts.server`](src/vitts/server.py) | FastAPI server tương thích OpenAI `/v1/audio/speech` |
| [`app.py`](app.py) | Demo Gradio |

## Phát triển

```bash
pip install -e ".[dev]"
pytest
ruff check . && ruff format --check .
```

Khi chạy benchmark trên GPU, chỉ định GPU bằng `CUDA_VISIBLE_DEVICES` (ví dụ `CUDA_VISIBLE_DEVICES=0`).

## Giấy phép

- Mã nguồn và bộ test: [MIT](LICENSE).
- Các thư viện và model được benchmark giữ giấy phép riêng. Ví dụ Meta MMS là CC-BY-NC 4.0, không dùng thương mại.

---

*English:* ViTTS-Bench is an open, reproducible benchmark for Vietnamese TTS. Stage 1 compares Vietnamese text normalizers on a hand-written held-out set (soe-vinorm currently leads at 76% sentence accuracy). Stage 2 will benchmark TTS models (intelligibility via ASR round-trip WER, RTF, VRAM) under one harness.
