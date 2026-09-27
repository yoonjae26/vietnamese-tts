#!/usr/bin/env bash
source "$(dirname "$0")/_common.sh"
make_env vitts-f5 3.11
SRC=$(clone nguyenthienhy/F5-TTS-Vietnamese HEAD)
$PIP install -q torch==2.6.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu124
$PIP install -q -e "$SRC"
