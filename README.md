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
| 🔊 Model TTS: độ rõ, lỗi không dừng, giống giọng, UTMOS, tốc độ, VRAM, giấy phép | ✅ 7 model |
| 🎧 [Trang nghe thử](https://yoonjae26.github.io/vietnamese-tts/listen/): 7 model đọc cùng câu, kèm lời ASR nghe được | ✅ |
| 🌐 API chung tương thích OpenAI, chọn model bằng tham số `model` | ✅ `vitts-server` |

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

## Kết quả: model TTS

50 câu chung, đã ở dạng đọc (không số, không viết tắt), nên chỉ đo chất lượng model. ASR [`vinai/PhoWhisper-large`](https://huggingface.co/vinai/PhoWhisper-large) nghe lại audio, rồi tính WER so với câu gốc. Mỗi model dùng tham số do tác giả khuyến nghị và seed cố định. Các model clone giọng dùng **chung một giọng mẫu**: 8 giây giọng thật của tác giả repo, ghi bằng điện thoại ([`benchmark/tts/reference/`](benchmark/tts/reference/)).

| Model | WER ↓ | WER câu ngắn | WER thanh điệu khó | Không dừng ↓ | Giống giọng ↑ | UTMOS ↑ | RTF ↓ | VRAM | Giấy phép |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| [IndexTTS-2 Vietnamese](https://huggingface.co/dinhthuan/index-tts-2-vietnamese) | **1.8%** | **0.0%** | **12.2%** | 0/50 | **0.741** | 1.99 | 1.063 | 8.9 GB | Apache-2.0* |
| [F5-TTS-Vietnamese-1000h](https://huggingface.co/hynt/F5-TTS-Vietnamese-ViVoice) | 3.0% | **0.0%** | 14.9% | 0/50 | 0.731 | 2.21 | 0.219 | 0.8 GB | CC-BY-NC-SA-4.0 |
| [VieNeu-TTS v3 Turbo](https://huggingface.co/pnnbao-ump/VieNeu-TTS-v3-Turbo) | 3.3% | 6.7% | 18.9% | 0/50 | 0.656 | 2.16 | 0.101 | 0.9 GB | **Apache-2.0** |
| [Piper vi_VN-vais1000-medium](https://huggingface.co/rhasspy/piper-voices) | 5.7% | 4.4% | 39.2% | 0/50 | (0.198) | 2.37 | 0.037 (CPU) | – | CC-BY-4.0 |
| [MMS-TTS (Meta)](https://huggingface.co/facebook/mms-tts-vie) | 6.9% | 11.1% | 28.4% | 0/50 | (0.318) | **2.74** | **0.013** | **0.4 GB** | CC-BY-NC-4.0 |
| [viXTTS](https://huggingface.co/capleaf/viXTTS) | 9.2% | 24.4% | 41.9% | 0/50 | 0.638 | 2.20 | 0.202 | 2.3 GB | CPML (NC) |
| [VietTTS](https://huggingface.co/dangvansam/viet-tts) | 12.0% | 13.3% | 41.9% | 0/50 | 0.728 | 2.39 | 0.395 | 1.7 GB | CC |

RTF đo trên NVIDIA H200 (Piper đo trên CPU). \* Dùng thương mại cần xin phép tác giả IndexTTS.

**Giống giọng** là cosine giữa embedding [ECAPA-TDNN](https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb) của giọng mẫu và của audio sinh ra. MMS và Piper không clone giọng, nên điểm của chúng (trong ngoặc) là mốc cho hai người nói khác nhau. Model `wavlm-base-plus-sv` từng được thử trước nhưng đã bỏ: nó cho một giọng nữ khác hẳn (Piper) 0.94, gần bằng các model clone, tức là gần như chỉ tách được giới tính.

**UTMOS** là điểm tự nhiên dự đoán (1 đến 5) của [UTMOS22](https://github.com/tarepan/SpeechMOS), model huấn luyện trên tiếng Anh. Model clone giọng bắt chước cả điều kiện ghi âm của giọng mẫu: giọng mẫu ghi bằng điện thoại chỉ được 1.82, nên điểm của các model clone thấp hơn MMS và Piper (giọng thu trong phòng thu). Chỉ dùng cột này để so sánh tương đối giữa các model clone.

### Giọng mẫu ảnh hưởng tới kết quả thế nào

Benchmark đã chạy với hai giọng mẫu. Lần đầu dùng giọng nữ trong file mẫu của repo viXTTS; lần hai dùng giọng thật của tác giả. Kết quả lần đầu lưu ở [`results/archive/`](results/archive/).

| | Giọng mẫu A: file mẫu của viXTTS | Giọng mẫu B: tác giả, ghi bằng điện thoại |
|---|---:|---:|
| IndexTTS-2: số câu không dừng | ⚠️ 5/50 | 0/50 |
| viXTTS: WER câu ngắn | 46.7% | 24.4% |
| viXTTS: giống giọng | 0.812 (cao nhất) | 0.638 (thấp nhất) |
| F5 / VieNeu / IndexTTS-2: WER | 2.3% / 2.8% / 1.9% | 3.0% / 3.3% / 1.8% |
| UTMOS của chính giọng mẫu | 2.41 | 1.82 |

- **Lỗi "không dừng" của IndexTTS-2 phụ thuộc giọng mẫu.** Với giọng A, nó đọc đúng rồi sinh thêm khoảng 28 giây im lặng ở 5/50 câu. ASR bỏ qua khoảng lặng nên WER không phát hiện được; đó là lý do bảng có cột "Không dừng" (số câu có giây/từ lớn hơn 3 lần trung vị của chính model). Với giọng B, lỗi này không xuất hiện.
- **viXTTS được lợi khi giọng mẫu lấy từ chính repo của nó.** Với một giọng lạ, độ giống giọng của nó tụt từ cao nhất xuống thấp nhất.
- **Thứ hạng WER của nhóm dẫn đầu ổn định** (IndexTTS-2, F5, VieNeu) qua cả hai giọng mẫu.
- Vì vậy một benchmark clone giọng đáng tin cần nhiều giọng mẫu (nam, nữ, phòng thu, điện thoại). Đây là việc tiếp theo trong lộ trình.

**Nhận xét**
- **IndexTTS-2 rõ nhất và giống giọng nhất**, nhưng chậm nhất (RTF 1.06, chậm hơn thời gian thực), tốn 8.9 GB VRAM, và có thể không dừng tùy giọng mẫu.
- **F5-TTS-Vietnamese ổn định**: rõ ở mọi nhóm câu, nhẹ (0.8 GB), nhưng giấy phép phi thương mại.
- **VieNeu-TTS v3 Turbo là lựa chọn cân bằng nhất cho sản phẩm**: WER 3.3%, nhanh (RTF 0.1), âm thanh 48 kHz và **giấy phép Apache-2.0**, cho phép dùng thương mại.
- **Piper và MMS** hợp với thiết bị yếu: rất nhanh, rõ ở câu thường, nhưng đọc kém câu nhiều thanh điệu khó.
- **viXTTS và VietTTS** đọc kém nhất trên bộ này, nhất là câu líu lưỡi (41.9%).
- Bảng đầy đủ: [`results/tts.md`](results/tts.md). Transcript từng câu: [`results/tts.json`](results/tts.json).
- **Hạn chế:** WER qua ASR đo *độ rõ*. Nhóm "thanh điệu khó" gồm các câu líu lưỡi, nên ASR cũng dễ nghe nhầm. Cần thêm bản ghi người đọc thật để biết mức lỗi nền của chính ASR.
- 🎧 **Nghe trực tiếp:** [trang nghe thử](https://yoonjae26.github.io/vietnamese-tts/listen/) ([`docs/listen`](docs/listen/)) cho 8 câu tiêu biểu, tô màu từ mà ASR nghe sai.

```bash
# tạo môi trường cho từng model (mã nguồn model được clone vào ~/vitts-engines)
bash benchmark/tts/envs/coqui.sh   # và f5.sh, vieneu.sh, viettts.sh, indextts.sh
# sinh audio cho tất cả model rồi chấm điểm (chỉ dùng GPU 0)
bash benchmark/tts/run_all.sh
```

## API chung tương thích OpenAI

Mỗi model chạy trong một worker riêng (môi trường riêng, vì thư viện của chúng xung đột nhau). `vitts-server` gom các worker lại thành một API `/v1/audio/speech`. Gateway tự chuẩn hóa văn bản tiếng Việt, tách câu, gửi tới model được chọn rồi ghép audio.

```bash
bash benchmark/tts/serve_all.sh vieneu f5 mms     # bật worker + gateway ở :8000 (chỉ GPU 0)
```

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="none")
client.audio.speech.create(model="vieneu", voice="default", input="Giá 100k, giao lúc 14h30 tại TP.HCM.").write_to_file(
    "out.wav"
)
```

| | |
| --- | --- |
| `model` | `vieneu`, `f5`, `indextts2`, `vixtts`, `viettts`, `mms`, `piper`. `tts-1` hoặc bỏ trống sẽ dùng model mặc định (model đầu tiên được bật). |
| `normalize` | `true` (mặc định): đọc số, ngày giờ, tiền, viết tắt trước khi gửi tới model. Văn bản sau chuẩn hóa trả về trong header `X-Normalized-Text`. |
| `response_format`, `speed`, `seed` | `wav` / `flac` / `pcm`; tốc độ 0.25 đến 4; seed cố định cho model sinh ngẫu nhiên. |
| `GET /v1/models`, `POST /v1/normalize` | Danh sách model đang bật; chỉ chuẩn hóa văn bản. |

Không có GPU? `vitts-server --local` chạy MMS ngay trong tiến trình, không cần worker.

## Lộ trình

**Giai đoạn 2: benchmark model TTS**
- [x] Bộ câu chung cho mọi model: câu ngắn, câu vừa, câu dài, thanh điệu khó, tên riêng
- [x] Độ rõ: ASR tiếng Việt (PhoWhisper) nghe lại audio → WER/CER, phát hiện lỗi không dừng
- [x] Tốc độ (RTF) và VRAM
- [ ] Thời gian ra audio đầu tiên khi streaming, RTF trên CPU cho mọi model
- [x] Độ giống giọng khi clone (ECAPA-TDNN), MOS dự đoán (UTMOS)
- [ ] MOS bằng người nghe tiếng Việt
- [ ] Nhiều giọng mẫu (nam, nữ, phòng thu, điện thoại): kết quả clone giọng thay đổi theo giọng mẫu
- [x] Các model: Meta MMS, viXTTS, VietTTS, F5-TTS-Vietnamese, VieNeu-TTS, IndexTTS-2, Piper
- [x] Trang nghe thử: cùng một câu, mọi model

**Giai đoạn 3: API chung**
- [x] Một server tương thích OpenAI, chọn model bằng tham số `model`
- [ ] Streaming audio, chọn giọng mẫu qua tham số `voice`

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
| [`vitts.server`](src/vitts/server.py) | Gateway tương thích OpenAI `/v1/audio/speech` cho mọi model |
| [`docs/listen`](docs/listen/) | Trang nghe thử (GitHub Pages); tạo lại bằng `python docs/listen/build.py` |
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

*English:* ViTTS-Bench is an open, reproducible benchmark for Vietnamese TTS. Stage 1 compares Vietnamese text normalizers on a hand-written held-out set (soe-vinorm currently leads at 76% sentence accuracy). Stage 2 benchmarks 7 TTS models (ASR round-trip WER, a runaway-generation check that WER misses, ECAPA speaker similarity, UTMOS, RTF, VRAM) with a listening page, and an OpenAI-compatible gateway serves all of them behind one `/v1/audio/speech` endpoint.
