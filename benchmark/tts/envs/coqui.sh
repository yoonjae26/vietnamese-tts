#!/usr/bin/env bash
# MMS, viXTTS, Piper + bộ chấm điểm (PhoWhisper)
source "$(dirname "$0")/_common.sh"
make_env vitts-coqui 3.11
$PIP install -q torch==2.6.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu124
$PIP install -q "coqui-tts==0.27.5" "transformers>=4.57,<5" jiwer soundfile librosa huggingface_hub "piper-tts==1.3.0" speechbrain
