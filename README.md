# 🇻🇳 ViTTS-Bench: Benchmark mở cho Text-to-Speech tiếng Việt

[![CI](https://github.com/yoonjae26/vietnamese-tts/actions/workflows/ci.yml/badge.svg)](https://github.com/yoonjae26/vietnamese-tts/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)

TTS tiếng Việt mã nguồn mở đã có nhiều lựa chọn (IndexTTS-2, F5-TTS, VieNeu-TTS, viXTTS, VietTTS, Piper, Meta MMS…), nhưng mỗi dự án tự báo cáo trên dữ liệu riêng. ViTTS-Bench so sánh chúng **trên cùng bộ test, cùng cách chấm, chạy lại được bằng một lệnh**, kèm bộ chuẩn hóa văn bản tiếng Việt và một API chung cho mọi model.

🎧 **[Nghe thử 7 model đọc cùng một câu](https://yoonjae26.github.io/vietnamese-tts/listen/)**

## Tóm tắt

- **Model TTS:** IndexTTS-2 rõ nhất (WER 1.8%) nhưng chậm hơn thời gian thực và tốn 8.9 GB VRAM. **VieNeu-TTS v3 Turbo cân bằng nhất cho sản phẩm** (WER 3.3%, nhanh gấp 10 lần thời gian thực, Apache-2.0).
- **WER không đủ:** IndexTTS-2 có lúc đọc đúng rồi sinh thêm ~28 giây im lặng mà WER không phát hiện, nên benchmark có thêm chỉ số "không dừng". **Kết quả clone giọng phụ thuộc giọng mẫu**: đổi giọng mẫu làm lỗi này biến mất, và làm độ giống giọng của viXTTS tụt từ cao nhất xuống thấp nhất.
- **Chuẩn hóa văn bản:** vitts 0.2 kèm model phiên âm đạt **70%** câu đọc đúng trên bộ held-out v2, so với 47% của bộ tốt nhất hiện có.
- **Model phiên âm từ nước ngoài (5.6M tham số):** theo người Việt duyệt mù, **ngang gpt-4o-mini** (24.8% so với 30.9%, chênh lệch không có ý nghĩa thống kê) và **tốt hơn Qwen2.5-7B** (14.8%), chạy cục bộ với 0.1 GB VRAM. Chính từ điển dùng để huấn luyện chỉ được chấp nhận 27.5%.
- **API chung:** một endpoint `/v1/audio/speech` tương thích OpenAI cho cả 7 model.

## Kết quả: model TTS

50 câu chung, đã ở dạng đọc (không số, không viết tắt), nên chỉ đo chất lượng model. ASR [`vinai/PhoWhisper-large`](https://huggingface.co/vinai/PhoWhisper-large) nghe lại audio, rồi tính WER so với câu gốc. Mỗi model dùng tham số do tác giả khuyến nghị và seed cố định. Các model clone giọng dùng **chung một giọng mẫu**: 8 giây giọng thật của tác giả repo, ghi bằng điện thoại ([`benchmark/tts/reference/`](benchmark/tts/reference/)).

| Model | WER ↓ | WER câu ngắn | WER thanh điệu khó | Không dừng ↓ | Giống giọng ↑ | UTMOS ↑ | RTF ↓ | VRAM | Giấy phép |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| [IndexTTS-2 Vietnamese](https://huggingface.co/dinhthuan/index-tts-2-vietnamese) | **1.8%** | **0.0%** | **12.2%** | 0/50 | **0.741** | 1.99 | 1.063 | 8.9 GB | Apache-2.0\* |
| [F5-TTS-Vietnamese-1000h](https://huggingface.co/hynt/F5-TTS-Vietnamese-ViVoice) | 3.0% | **0.0%** | 14.9% | 0/50 | 0.731 | 2.21 | 0.219 | 0.8 GB | CC-BY-NC-SA-4.0 |
| [VieNeu-TTS v3 Turbo](https://huggingface.co/pnnbao-ump/VieNeu-TTS-v3-Turbo) | 3.3% | 6.7% | 18.9% | 0/50 | 0.656 | 2.16 | 0.101 | 0.9 GB | **Apache-2.0** |
| [Piper vi_VN-vais1000-medium](https://huggingface.co/rhasspy/piper-voices) | 5.7% | 4.4% | 39.2% | 0/50 | (0.198) | 2.37 | 0.037 (CPU) | – | CC-BY-4.0 |
| [MMS-TTS (Meta)](https://huggingface.co/facebook/mms-tts-vie) | 6.9% | 11.1% | 28.4% | 0/50 | (0.318) | **2.74** | **0.013** | **0.4 GB** | CC-BY-NC-4.0 |
| [viXTTS](https://huggingface.co/capleaf/viXTTS) | 9.2% | 24.4% | 41.9% | 0/50 | 0.638 | 2.20 | 0.202 | 2.3 GB | CPML (NC) |
| [VietTTS](https://huggingface.co/dangvansam/viet-tts) | 12.0% | 13.3% | 41.9% | 0/50 | 0.728 | 2.39 | 0.395 | 1.7 GB | CC |

RTF đo trên NVIDIA H200 (Piper đo trên CPU). \* Dùng thương mại cần xin phép tác giả IndexTTS. Bảng đầy đủ: [`results/tts.md`](results/tts.md); transcript từng câu: [`results/tts.json`](results/tts.json).

- **Không dừng:** số câu có giây/từ lớn hơn 3 lần trung vị của chính model, tức model sinh thừa khoảng lặng hoặc âm rác. ASR bỏ qua khoảng lặng nên WER không bắt được lỗi này.
- **Giống giọng:** cosine giữa embedding [ECAPA-TDNN](https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb) của giọng mẫu và audio sinh ra. MMS và Piper không clone giọng, nên điểm của chúng (trong ngoặc) là mốc cho hai người nói khác nhau. `wavlm-base-plus-sv` đã được thử trước rồi bỏ: nó cho một giọng nữ khác hẳn (Piper) 0.94, gần bằng các model clone, tức là gần như chỉ tách được giới tính.
- **UTMOS:** điểm tự nhiên dự đoán (1 đến 5) của [UTMOS22](https://github.com/tarepan/SpeechMOS), huấn luyện trên tiếng Anh. Model clone giọng bắt chước cả điều kiện ghi âm: giọng mẫu ghi bằng điện thoại chỉ được 1.82, nên các model clone thấp hơn MMS và Piper. Chỉ dùng để so sánh tương đối giữa các model clone.

**Nhận xét**
- **IndexTTS-2** rõ nhất và giống giọng nhất, nhưng chậm nhất (RTF 1.06), tốn VRAM nhất, và có thể không dừng tùy giọng mẫu (xem bên dưới).
- **F5-TTS-Vietnamese** ổn định ở mọi nhóm câu và nhẹ, nhưng giấy phép phi thương mại.
- **VieNeu-TTS v3 Turbo** là lựa chọn cân bằng nhất cho sản phẩm: WER 3.3%, RTF 0.1, âm thanh 48 kHz, Apache-2.0.
- **Piper và MMS** hợp với thiết bị yếu: rất nhanh, rõ ở câu thường, nhưng kém ở câu nhiều thanh điệu khó.
- **viXTTS và VietTTS** đọc kém nhất trên bộ này, nhất là câu líu lưỡi (41.9%).
- **Hạn chế:** WER qua ASR chỉ đo *độ rõ*. Câu líu lưỡi khó với cả ASR. Cần bản ghi người đọc thật để biết mức lỗi nền của chính ASR, và MOS do người nghe chấm.

### Giọng mẫu ảnh hưởng tới kết quả

Benchmark đã chạy với hai giọng mẫu. Kết quả lần đầu lưu ở [`results/archive/`](results/archive/).

| | Giọng mẫu A: file mẫu của viXTTS | Giọng mẫu B: tác giả, ghi bằng điện thoại |
|---|---:|---:|
| IndexTTS-2: số câu không dừng | ⚠️ 5/50 | 0/50 |
| viXTTS: WER câu ngắn | 46.7% | 24.4% |
| viXTTS: giống giọng | 0.812 (cao nhất) | 0.638 (thấp nhất) |
| F5 / VieNeu / IndexTTS-2: WER | 2.3% / 2.8% / 1.9% | 3.0% / 3.3% / 1.8% |
| UTMOS của chính giọng mẫu | 2.41 | 1.82 |

- Lỗi "không dừng" của IndexTTS-2 phụ thuộc giọng mẫu: với giọng A, nó đọc đúng rồi sinh thêm khoảng 28 giây im lặng ở 5/50 câu.
- viXTTS được lợi khi giọng mẫu lấy từ chính repo của nó.
- Thứ hạng WER của nhóm dẫn đầu ổn định qua cả hai giọng mẫu. Một benchmark clone giọng đáng tin cần nhiều giọng mẫu hơn (nam, nữ, phòng thu, điện thoại).

## Kết quả: chuẩn hóa văn bản

Model TTS chỉ đọc được chữ, nên `"100k"`, `"14h30"`, `"TP.HCM"`, `"iPhone"` phải được đổi sang cách đọc trước. Bước này sai thì model tốt đến đâu cũng đọc sai.

**Bộ held-out v2** (60 câu, [commit trước mọi thay đổi của vitts 0.2](benchmark/normalization/build_testset.py)) là con số chính thức. Ô là **tỉ lệ câu đọc đúng hoàn toàn** (WER trong ngoặc):

| Nhóm | n | vitts 0.2 (quy tắc) | **vitts 0.2 + phiên âm** | vinorm 2.0.7 | soe-vinorm 0.3.2 | vietnormalizer 0.2.3 |
|---|---:|---:|---:|---:|---:|---:|
| foreign | 18 | 0% (38.1%) | **67% (6.7%)** | 0% (38.1%) | 0% (38.1%) | 61% (8.6%) |
| names | 7 | 0% (61.1%) | 43% (18.9%) | 0% (61.1%) | 0% (61.1%) | **57% (13.5%)** |
| acronym | 12 | 50% (27.1%) | **75% (9.4%)** | 0% (38.8%) | 25% (27.5%) | 50% (25.0%) |
| number | 4 | **100% (0.0%)** | **100% (0.0%)** | 50% (8.0%) | 75% (4.0%) | 25% (20.0%) |
| unit | 4 | **100% (0.0%)** | **100% (0.0%)** | 25% (22.6%) | 50% (6.5%) | 0% (46.4%) |
| abbreviation | 4 | **100% (0.0%)** | **100% (0.0%)** | **100% (0.0%)** | **100% (0.0%)** | 0% (48.3%) |
| plain | 6 | **83% (5.7%)** | **83% (2.9%)** | **83% (5.7%)** | **83% (5.7%)** | **83% (2.9%)** |
| mixed | 5 | 0% (45.9%) | **20% (11.5%)** | 0% (45.9%) | 0% (45.9%) | **20% (11.5%)** |
| **Tổng** | 60 | 38% (28.3%) | **70% (7.4%)** | 20% (32.8%) | 28% (29.1%) | 47% (18.6%) |
| ms / câu | | 0.2 | 296.3 | 30.1 | 0.4 | 0.4 |

- **vitts 0.2 + model phiên âm đứng đầu (70%)**, nhất là ở từ nước ngoài và chữ viết tắt. Không có model, vitts chỉ đạt 38%.
- **vietnormalizer mạnh hơn ở tên riêng** (57% so với 43%) nhờ từ điển 17.7k từ.
- **Đã gặp và chưa gặp:** model được huấn luyện trên từ điển của vietnormalizer, nên 32/55 từ nước ngoài trong v2 đã có trong phần train. Trên 22 câu mà mọi từ nước ngoài đều chưa gặp: vitts + phiên âm 64%, vietnormalizer 50%.
- **Tốc độ là điểm yếu:** khoảng 300 ms mỗi câu trên CPU khi câu có nhiều từ nước ngoài, vì mỗi từ được giải mã riêng.

<details>
<summary>Bộ held-out v1 (59 câu) và dev (99 câu)</summary>

| Bộ | vitts 0.1 | vitts 0.2 | vitts 0.2 + phiên âm | vinorm | soe-vinorm | vietnormalizer |
|---|---:|---:|---:|---:|---:|---:|
| held-out v1 | 59% | 85%\* | 86%\* | 59% | 76% | 44% |
| dev | 100%\* | 100%\* | 100%\* | 83% | 90% | 66% |

\* Không còn là số đo khách quan: vitts 0.1 được sửa theo bộ dev, và các quy tắc của vitts 0.2 được viết sau khi xem lỗi trên v1.
</details>

**Phương pháp.** Mỗi phiên bản của vitts được đo trên một bộ held-out **viết trước** khi phiên bản đó được phát triển, và không sửa code theo bộ đó (lịch sử git cho thấy thứ tự này). Đáp án được viết tay, một câu có thể có nhiều đáp án, và các biến thể vùng miền (*ngàn/nghìn, lẻ/linh, tỉ/tỷ…*) được quy về một dạng ([`metrics.py`](src/vitts/bench/metrics.py)). **Hạn chế:** bộ test do một người viết và còn nhỏ. Kết quả từng câu: [`results/normalization_heldout_v2_errors.md`](results/normalization_heldout_v2_errors.md).

## Model phiên âm từ nước ngoài

`vitts.translit` là một transformer seq2seq 5.6M tham số, đọc từng ký tự của từ (kèm âm vị [CMUdict](https://github.com/cmusphinx/cmudict) nếu có), và sinh cách đọc tiếng Việt: "container" → "công tê nơ". Model được huấn luyện trên 17.7k cặp từ viết tay của [vietnormalizer](https://github.com/nghimestudio/vietnormalizer) (MIT), chia train/dev/test **theo gốc từ**, và cấu hình được chọn chỉ dựa trên dev.

```python
from vitts import normalize_text

normalize_text("Họp online qua Zoom, rút tiền ở ATM.", translit="auto")
```

### Đánh giá bằng người duyệt mù

150 từ ngẫu nhiên trong bộ test được một người Việt duyệt: người duyệt thấy mọi cách đọc (từ điển, model của repo, gpt-4o-mini, Qwen, quy tắc, và 3 cách GPT gợi ý thêm) đã xáo trộn, không biết cách nào của hệ thống nào, rồi chọn cách chấp nhận được ([trang duyệt](https://yoonjae26.github.io/vietnamese-tts/review/), [mã nguồn](docs/review/), [dữ liệu](data/translit/review/)).

| Hệ thống | Đúng theo người duyệt (149 từ) | KTC 95% |
|---|---:|---:|
| gpt-4o-mini few-shot (OpenAI API) | **30.9%** | 23.5–38.3% |
| gpt-4o-mini zero-shot | 30.2% | |
| Đáp án gốc của từ điển | 27.5% | 20.8–34.9% |
| **vitts translit (5.6M tham số, 0.1 GB VRAM)** | **24.8%** | 18.1–32.2% |
| Qwen2.5-7B-Instruct few-shot (7.6B tham số) | 14.8% | 9.4–20.8% |
| vietnormalizer (quy tắc) | 4.0% | |

- **Ngang gpt-4o-mini:** GPT hơn 6 điểm, nhưng khoảng tin cậy của chênh lệch là −4% đến +16%, nên chưa kết luận được bên nào tốt hơn.
- **Tốt hơn Qwen2.5-7B có ý nghĩa thống kê** (+10 điểm, KTC 95% +0.7% đến +19.5%). Qwen giữ nguyên tiếng Anh, chèn chữ Hán, hoặc bịa ký tự ([output thô](results/translit_llm_raw_examples.txt)).
- **Chính từ điển dùng để huấn luyện chỉ được chấp nhận 27.5%**, và model học theo nó nên đạt mức tương đương.
- **Hạn chế:** chỉ một người duyệt; người duyệt thường chọn một cách ưa dùng nhất (138/150 từ); mỗi từ có tới 5 ứng viên theo phong cách GPT, so với 1 của mỗi hệ thống khác.

<details>
<summary>Chấm tự động theo đáp án của từ điển (1.676 từ chưa gặp)</summary>

| Hệ thống | Đúng cả từ ↑ | Lỗi âm tiết ↓ |
|---|---:|---:|
| soe-vinorm | 0.5% | 110.5% |
| vietnormalizer (quy tắc, không tra từ điển) | 7.8% | 73.1% |
| vitts translit v1 (chỉ chữ) | 47.1% | 37.2% |
| **vitts translit (chữ + âm vị CMUdict)** | **55.1%** | **30.0%** |
| Qwen2.5-7B-Instruct zero-shot / few-shot | 3.2% / 4.2% | 95.3% / 95.9% |
| gpt-4o-mini zero-shot / few-shot | 15.9% / 19.6% | 75.5% / 66.4% |

Cách chấm này thiên về model của repo, vì model học đúng quy ước viết của từ điển ("s" → "x", "f" → "ph"), trong khi GPT viết "sam sung", "nét flích" và bị chấm sai. Vì vậy kết quả người duyệt ở trên là con số chính. Đánh giá gpt-4o-mini trên 1.676 từ tốn khoảng 67 nghìn token ([script](training/translit/api_baseline.py)).

| Cấu hình (dò trên dev) | Dev |
|---|---:|
| d256, 3 lớp, dropout 0.1 | 47.3% |
| d256, 3 lớp, dropout 0.2 | 51.7% |
| d384, 4 lớp, dropout 0.2 | 52.3% |
| **d256, 3 lớp, dropout 0.2, + âm vị** (được chọn) | **53.1%** |
| d384, 4 lớp, dropout 0.2, + âm vị | 53.1% |
</details>

### Thử nghiệm: gắn nhãn lại bằng GPT (kết quả âm)

16 nghìn từ train/dev được gắn nhãn lại bằng gpt-4o-mini (khoảng 390 nghìn token, [script](training/translit/relabel_gpt.py)), rồi huấn luyện lại với đúng cấu hình cũ và chấm một lần trên 149 từ đã duyệt:

| Nhãn huấn luyện | Đúng theo người duyệt | So với gpt-4o-mini (KTC 95%) |
|---|---:|---:|
| **Từ điển (mặc định)** | **24.8%** | −6.0% (−16.1% đến +4.0%) |
| Từ điển + GPT | 24.2% | −6.7% (−16.1% đến +2.7%) |
| Chỉ GPT | 12.8% | −18.1% (−24.8% đến −11.4%) |

Nhãn GPT làm model **kém đi một nửa**: 11% nhãn còn lẫn chữ Latin ("blai th"), và GPT đọc từng từ theo hiểu biết riêng thay vì một quy tắc nhất quán, nên model nhỏ học được phần nhiễu mà không học được phần hiểu biết. Muốn cải thiện thật cần nhãn do người gắn, nhất quán, và nhiều người duyệt hơn.

## API chung tương thích OpenAI

Mỗi model chạy trong một worker riêng (môi trường riêng, vì thư viện của chúng xung đột nhau). `vitts-server` gom các worker thành một API `/v1/audio/speech`: tự chuẩn hóa văn bản tiếng Việt, tách câu, gửi tới model được chọn rồi ghép audio.

```bash
bash benchmark/tts/serve_all.sh vieneu f5 mms     # bật worker + gateway ở :8000 (chỉ GPU 0)
```

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="none")
speech = client.audio.speech.create(model="vieneu", voice="default", input="Giá 100k, giao lúc 14h30 tại TP.HCM.")
speech.write_to_file("out.wav")
```

| Tham số | |
| --- | --- |
| `model` | `vieneu`, `f5`, `indextts2`, `vixtts`, `viettts`, `mms`, `piper`. `tts-1` hoặc bỏ trống: model đầu tiên được bật. |
| `normalize` | `true` (mặc định): đọc số, ngày giờ, tiền, viết tắt trước khi gửi tới model. Văn bản sau chuẩn hóa trả về trong header `X-Normalized-Text`. |
| `response_format`, `speed`, `seed` | `wav` / `flac` / `pcm`; tốc độ 0.25 đến 4; seed cho model sinh ngẫu nhiên. |
| `GET /v1/models`, `POST /v1/normalize` | Danh sách model đang bật; chỉ chuẩn hóa văn bản. |

`voice` được chấp nhận để tương thích OpenAI nhưng hiện mỗi model dùng giọng mặc định của nó. Không có GPU? `vitts-server --local` chạy MMS ngay trong tiến trình.

## Chạy lại

```bash
git clone https://github.com/yoonjae26/vietnamese-tts.git && cd vietnamese-tts
pip install -e ".[bench,translit]"

# chuẩn hóa văn bản
python benchmark/normalization/build_testset.py
python benchmark/normalization/run.py --split heldout_v2

# model TTS: mỗi model một môi trường conda (mã nguồn model được clone vào ~/vitts-engines)
bash benchmark/tts/envs/coqui.sh      # và f5.sh, vieneu.sh, viettts.sh, indextts.sh
bash benchmark/tts/run_all.sh         # sinh audio cho mọi model rồi chấm điểm

# model phiên âm
python training/translit/prepare_data.py
bash training/translit/sweep.sh
CUDA_VISIBLE_DEVICES=0 python training/translit/evaluate.py
```

Script GPU tự từ chối chạy nếu `CUDA_VISIBLE_DEVICES` khác `0`; sửa hằng số `ALLOWED_GPU` trong [`synthesize.py`](benchmark/tts/synthesize.py) nếu máy của bạn khác.

## Lộ trình

- [ ] MOS do người nghe tiếng Việt chấm; nhiều giọng mẫu (nam, nữ, phòng thu, điện thoại)
- [ ] Thời gian ra audio đầu tiên khi streaming; RTF trên CPU cho mọi model
- [ ] API: streaming audio, chọn giọng mẫu qua `voice`
- [ ] Phiên âm: nhãn do nhiều người gắn; tăng tốc (giải mã theo lô, ONNX); tên riêng không phải tiếng Anh
- [ ] Chuẩn hóa: bộ held-out v3 do nhiều người viết

## Cấu trúc repo

| Thành phần | Mô tả |
| --- | --- |
| [`benchmark/tts/`](benchmark/tts/) | Bộ câu, adapter cho 7 model, chấm điểm (WER, không dừng, giống giọng, UTMOS), worker cho API |
| [`benchmark/normalization/`](benchmark/normalization/) | Bộ test dev / held-out v1 / held-out v2 và script so sánh các bộ chuẩn hóa |
| [`src/vitts/text/`](src/vitts/text/) | Bộ chuẩn hóa tiếng Việt (phần quy tắc không cần thư viện ngoài) |
| [`src/vitts/translit/`](src/vitts/translit/), [`training/translit/`](training/translit/) | Model phiên âm, huấn luyện, đánh giá, so với LLM |
| [`src/vitts/server.py`](src/vitts/server.py) | Gateway tương thích OpenAI |
| [`docs/listen/`](docs/listen/) | Trang nghe thử (GitHub Pages), tạo lại bằng `python docs/listen/build.py` |
| [`docs/review/`](docs/review/) | Trang duyệt mù cách đọc (GitHub Pages); tiến độ lưu trong trình duyệt, xuất `reviews.jsonl` |
| [`results/`](results/) | Mọi bảng kết quả và output từng câu |

## Phát triển

```bash
pip install -e ".[dev]"
pytest
ruff check . && ruff format --check .
```

## Giấy phép và nguồn

- Mã nguồn và bộ test: [MIT](LICENSE).
- Dữ liệu phiên âm lấy từ [vietnormalizer](https://github.com/nghimestudio/vietnormalizer) (MIT, [giấy phép](data/translit/LICENSE-vietnormalizer)).
- Giọng mẫu trong `benchmark/tts/reference/` là giọng của tác giả repo, được công khai để phục vụ benchmark.
- Các model được benchmark giữ giấy phép riêng (xem bảng). Nhiều model không cho dùng thương mại.

---

*English:* ViTTS-Bench is an open, reproducible benchmark for Vietnamese TTS. It compares 7 open models on one shared sentence set (ASR round-trip WER, a runaway-generation check that WER misses, ECAPA speaker similarity, UTMOS, RTF, VRAM), shows that voice-cloning results depend on the reference voice, and serves every model behind one OpenAI-compatible `/v1/audio/speech` gateway. The bundled normalizer vitts 0.2, with a 5.6M-parameter loanword transliteration model, leads a held-out set at 70% sentence accuracy (next best 47%). In a blind human review the transliteration model is on par with gpt-4o-mini (24.8% vs 30.9%, not significant) and better than Qwen2.5-7B (14.8%).
