# Benchmark TTS tiếng Việt (2026-09-28)

ASR chấm điểm: `vinai/PhoWhisper-large`. 50 câu. WER/CER càng thấp càng rõ. RTF = thời gian sinh / độ dài audio (càng thấp càng nhanh). **Không dừng** = số câu có giây/từ > 3× trung vị của model (sinh thừa khoảng lặng hoặc âm rác; WER không phát hiện được). **UTMOS** = điểm tự nhiên dự đoán 1–5 (model huấn luyện trên tiếng Anh, chỉ so sánh tương đối). **SIM** = độ giống giọng mẫu (cosine ECAPA-TDNN). MMS và Piper không clone giọng (giọng cố định của người khác), SIM của chúng là mốc cho hai người nói khác nhau. Chính giọng mẫu: UTMOS 1.82.

| Model | WER | CER | WER short | WER medium | WER long | WER tones | WER names | Không dừng | UTMOS | SIM | RTF | VRAM | Hz | Giấy phép |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| [IndexTTS-2 Vietnamese](https://huggingface.co/dinhthuan/index-tts-2-vietnamese) | **1.8%** | 0.5% | 0.0% | 0.9% | 0.5% | 12.2% | 1.7% | 0/50 | 1.99 | 0.741 | 1.063 | 8.9 GB | 22050 | Apache-2.0 (dùng thương mại cần phép của IndexTTS) |
| [F5-TTS-Vietnamese-1000h](https://huggingface.co/hynt/F5-TTS-Vietnamese-ViVoice) | **3.0%** | 1.5% | 0.0% | 2.7% | 1.1% | 14.9% | 3.4% | 0/50 | 2.21 | 0.731 | 0.219 | 0.8 GB | 24000 | CC-BY-NC-SA-4.0 |
| [VieNeu-TTS v3 Turbo](https://huggingface.co/pnnbao-ump/VieNeu-TTS-v3-Turbo) | **3.3%** | 1.4% | 6.7% | 1.8% | 1.4% | 18.9% | 0.9% | 0/50 | 2.16 | 0.656 | 0.101 | 0.9 GB | 48000 | Apache-2.0 |
| [Piper vi_VN-vais1000-medium](https://huggingface.co/rhasspy/piper-voices) | **5.7%** | 2.9% | 4.4% | 0.9% | 1.9% | 39.2% | 6.0% | 0/50 | 2.37 | (0.198) | 0.037 | – (CPU) | 22050 | CC-BY-4.0 (dữ liệu VAIS-1000) |
| [MMS-TTS (Meta)](https://huggingface.co/facebook/mms-tts-vie) | **6.9%** | 3.4% | 11.1% | 5.4% | 3.5% | 28.4% | 5.1% | 0/50 | 2.74 | (0.318) | 0.013 | 0.4 GB | 16000 | CC-BY-NC-4.0 |
| [viXTTS](https://huggingface.co/capleaf/viXTTS) | **9.2%** | 5.2% | 24.4% | 4.9% | 3.8% | 41.9% | 7.7% | 0/50 | 2.20 | 0.638 | 0.202 | 2.3 GB | 24000 | CPML (non-commercial) |
| [VietTTS](https://huggingface.co/dangvansam/viet-tts) | **12.0%** | 6.9% | 13.3% | 7.1% | 8.2% | 41.9% | 13.7% | 0/50 | 2.39 | 0.728 | 0.395 | 1.7 GB | 22050 | CC (model card) |

GPU: NVIDIA H200 NVL.

