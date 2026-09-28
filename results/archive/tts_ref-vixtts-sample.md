# Vietnamese TTS benchmark (2026-09-27)

Scored by ASR `vinai/PhoWhisper-large` on 50 sentences; lower WER/CER is clearer. RTF = synthesis time / audio length (lower is faster). **Runaway** = sentences with seconds-per-word > 3× the model's median (extra silence or noise that WER cannot see). **UTMOS** = predicted naturalness 1–5 (trained on English; compare relatively). **SIM** = similarity to the reference voice (ECAPA-TDNN cosine). MMS and Piper do not clone voices, so their SIM is a different-speaker baseline. The reference itself scores UTMOS 2.41.

| Model | WER | CER | WER short | WER medium | WER long | WER tones | WER names | Runaway | UTMOS | SIM | RTF | VRAM | Hz | License |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| [IndexTTS-2 Vietnamese](https://huggingface.co/dinhthuan/index-tts-2-vietnamese) | **1.9%** | 0.9% | 0.0% | 0.4% | 0.3% | 14.9% | 2.6% | 5/50 | 2.79 | 0.722 | 0.780 | 8.9 GB | 22050 | Apache-2.0 (commercial use needs IndexTTS permission) |
| [F5-TTS-Vietnamese-1000h](https://huggingface.co/hynt/F5-TTS-Vietnamese-ViVoice) | **2.3%** | 0.8% | 0.0% | 1.3% | 1.9% | 9.5% | 1.7% | 0/50 | 3.17 | 0.758 | 0.277 | 0.8 GB | 24000 | CC-BY-NC-SA-4.0 |
| [VieNeu-TTS v3 Turbo](https://huggingface.co/pnnbao-ump/VieNeu-TTS-v3-Turbo) | **2.8%** | 1.2% | 4.4% | 1.8% | 0.5% | 13.5% | 4.3% | 0/50 | 2.98 | 0.734 | 0.101 | 0.9 GB | 48000 | Apache-2.0 |
| [Piper vi_VN-vais1000-medium](https://huggingface.co/rhasspy/piper-voices) | **5.7%** | 2.9% | 4.4% | 0.9% | 1.9% | 39.2% | 6.0% | 0/50 | 2.37 | (0.169) | 0.037 | – (CPU) | 22050 | CC-BY-4.0 (VAIS-1000 data) |
| [MMS-TTS (Meta)](https://huggingface.co/facebook/mms-tts-vie) | **6.9%** | 3.4% | 11.1% | 5.4% | 3.5% | 28.4% | 5.1% | 0/50 | 2.74 | (0.114) | 0.013 | 0.4 GB | 16000 | CC-BY-NC-4.0 |
| [viXTTS](https://huggingface.co/capleaf/viXTTS) | **9.4%** | 5.5% | 46.7% | 4.9% | 3.5% | 35.1% | 6.0% | 1/50 | 2.60 | 0.812 | 0.193 | 2.2 GB | 24000 | CPML (non-commercial) |
| [VietTTS](https://huggingface.co/dangvansam/viet-tts) | **12.0%** | 6.5% | 13.3% | 9.4% | 7.6% | 48.6% | 6.8% | 0/50 | 3.16 | 0.766 | 0.486 | 1.7 GB | 22050 | CC (see model card) |

GPU: NVIDIA H200 NVL.

- IndexTTS-2 Vietnamese: runaway sentences: short-03, short-07, short-08, short-09, tones-07
- viXTTS: runaway sentences: short-09
