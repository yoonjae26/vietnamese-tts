#!/usr/bin/env bash
# Theo README của VieNeu-TTS (GPU): torch 2.8.0 cu128 + transformers 4.57.6
source "$(dirname "$0")/_common.sh"
make_env vitts-vieneu 3.11
SRC=$(clone pnnbao97/VieNeu-TTS HEAD)
$PIP install -q torch==2.8.0 torchaudio==2.8.0 --index-url https://download.pytorch.org/whl/cu128
$PIP install -q "transformers==4.57.6"
# transformers 4.57.6 cần huggingface_hub < 1.0
$PIP install -q -e "$SRC" soundfile "huggingface_hub>=0.34,<1.0"
