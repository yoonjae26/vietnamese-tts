#!/usr/bin/env bash
# Fork tiếng Việt của IndexTTS-2. WeTextProcessing cần pynini (lấy từ conda-forge).
source "$(dirname "$0")/_common.sh"
make_env vitts-indextts 3.10
SRC=$(clone iamdinhthuan/index-tts-finetune-vietnamese HEAD)
"$CONDA" install -y -q -n vitts-indextts -c conda-forge "pynini=2.1.6"
$PIP install -q torch==2.6.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu124
$PIP install -q -e "$SRC"
