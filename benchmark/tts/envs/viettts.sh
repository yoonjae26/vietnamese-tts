#!/usr/bin/env bash
# Theo README của VietTTS: Python 3.10, pip install -e . (torch 2.0.1 được ghim trong pyproject)
source "$(dirname "$0")/_common.sh"
make_env vitts-viettts 3.10
SRC=$(clone dangvansam/viet-tts HEAD)
$PIP install -q torch==2.0.1 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118
# openai-whisper build cần pkg_resources, đã bị gỡ khỏi setuptools >= 81
$PIP install -q "setuptools<81" wheel
$PIP install -q --no-build-isolation "openai-whisper==20240930"
$PIP install -q -e "$SRC"
# hyperpyyaml hỏng với ruamel.yaml >= 0.18 ('Loader' object has no attribute 'max_depth')
$PIP install -q "ruamel.yaml<0.18"
# silero-vad kéo theo onnxruntime (CPU), che mất onnxruntime-gpu mà tác giả ghim
$PIP uninstall -y -q onnxruntime onnxruntime-gpu
$PIP install -q "onnxruntime-gpu==1.16.0"
