# Vietnamese TTS benchmark (2026-09-28)

Scored by ASR `vinai/PhoWhisper-large` on 50 sentences; lower WER/CER is clearer. RTF = synthesis time / audio length (lower is faster). **Runaway** = sentences with seconds-per-word > 3× the model's median (extra silence or noise that WER cannot see). **UTMOS** = predicted naturalness 1–5 (trained on English; compare relatively). **SIM** = similarity to the reference voice (ECAPA-TDNN cosine). MMS and Piper do not clone voices, so their SIM is a different-speaker baseline. The reference itself scores UTMOS 1.82.

| Model | WER | CER | WER short | WER medium | WER long | WER tones | WER names | Runaway | UTMOS | SIM | RTF | VRAM | Hz | License |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| [IndexTTS-2 Vietnamese](https://huggingface.co/dinhthuan/index-tts-2-vietnamese) | **1.8%** | 0.5% | 0.0% | 0.9% | 0.5% | 12.2% | 1.7% | 0/50 | 1.99 | 0.741 | 1.063 | 8.9 GB | 22050 | Apache-2.0 (commercial use needs IndexTTS permission) |
| [F5-TTS-Vietnamese-1000h](https://huggingface.co/hynt/F5-TTS-Vietnamese-ViVoice) | **3.0%** | 1.5% | 0.0% | 2.7% | 1.1% | 14.9% | 3.4% | 0/50 | 2.21 | 0.731 | 0.219 | 0.8 GB | 24000 | CC-BY-NC-SA-4.0 |
| [VieNeu-TTS v3 Turbo](https://huggingface.co/pnnbao-ump/VieNeu-TTS-v3-Turbo) | **3.3%** | 1.4% | 6.7% | 1.8% | 1.4% | 18.9% | 0.9% | 0/50 | 2.16 | 0.656 | 0.101 | 0.9 GB | 48000 | Apache-2.0 |
| [Piper vi_VN-vais1000-medium](https://huggingface.co/rhasspy/piper-voices) | **5.7%** | 2.9% | 4.4% | 0.9% | 1.9% | 39.2% | 6.0% | 0/50 | 2.37 | (0.198) | 0.037 | – (CPU) | 22050 | CC-BY-4.0 (VAIS-1000 data) |
| [MMS-TTS (Meta)](https://huggingface.co/facebook/mms-tts-vie) | **6.9%** | 3.4% | 11.1% | 5.4% | 3.5% | 28.4% | 5.1% | 0/50 | 2.74 | (0.318) | 0.013 | 0.4 GB | 16000 | CC-BY-NC-4.0 |
| [viXTTS](https://huggingface.co/capleaf/viXTTS) | **9.2%** | 5.2% | 24.4% | 4.9% | 3.8% | 41.9% | 7.7% | 0/50 | 2.20 | 0.638 | 0.202 | 2.3 GB | 24000 | CPML (non-commercial) |
| [VietTTS](https://huggingface.co/dangvansam/viet-tts) | **12.0%** | 6.9% | 13.3% | 7.1% | 8.2% | 41.9% | 13.7% | 0/50 | 2.39 | 0.728 | 0.395 | 1.7 GB | 22050 | CC (see model card) |

GPU: NVIDIA H200 NVL.

