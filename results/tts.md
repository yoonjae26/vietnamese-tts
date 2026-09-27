# Benchmark TTS tiếng Việt (2026-09-27)

ASR chấm điểm: `vinai/PhoWhisper-large`. 50 câu. WER/CER càng thấp càng rõ. RTF = thời gian sinh / độ dài audio (càng thấp càng nhanh).

| Model | WER | CER | WER short | WER medium | WER long | WER tones | WER names | RTF | VRAM | Hz | Giấy phép |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| [F5-TTS-Vietnamese-1000h](https://huggingface.co/hynt/F5-TTS-Vietnamese-ViVoice) | **2.3%** | 0.8% | 0.0% | 1.3% | 1.9% | 9.5% | 1.7% | 0.277 | 0.8 GB | 24000 | CC-BY-NC-SA-4.0 |
| [MMS-TTS (Meta)](https://huggingface.co/facebook/mms-tts-vie) | **6.9%** | 3.4% | 11.1% | 5.4% | 3.5% | 28.4% | 5.1% | 0.013 | 0.4 GB | 16000 | CC-BY-NC-4.0 |
| [viXTTS](https://huggingface.co/capleaf/viXTTS) | **9.4%** | 5.5% | 46.7% | 4.9% | 3.5% | 35.1% | 6.0% | 0.193 | 2.2 GB | 24000 | CPML (non-commercial) |

Thiết bị: NVIDIA H200 NVL.
