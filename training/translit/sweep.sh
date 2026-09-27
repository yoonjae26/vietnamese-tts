#!/usr/bin/env bash
# Dò cấu hình model phiên âm, chọn theo bộ dev (không nhìn bộ test). Chỉ GPU 0.
export CUDA_VISIBLE_DEVICES=0
cd "$(dirname "$0")/../.."
PY="$HOME/miniconda3/envs/vitts-coqui/bin/python"
OUT=models/translit/sweep
mkdir -p "$OUT" outputs/logs
run() {  # run <tên> <tham số...>
  local name=$1; shift
  "$PY" training/translit/train.py --out "$OUT/$name.pt" "$@" > "outputs/logs/sweep_$name.log" 2>&1
  echo "[$(date +%T)] $name: $(grep DONE "outputs/logs/sweep_$name.log" || echo FAIL)"
}
run d256_l3_do01            --d-model 256 --layers 3 --dropout 0.1 --epochs 150
run d256_l3_do02            --d-model 256 --layers 3 --dropout 0.2 --epochs 200
run d384_l4_do02            --d-model 384 --layers 4 --dropout 0.2 --epochs 200
run d256_l3_do02_ph         --d-model 256 --layers 3 --dropout 0.2 --epochs 200 --phonemes
run d384_l4_do02_ph         --d-model 384 --layers 4 --dropout 0.2 --epochs 200 --phonemes
echo "SWEEP DONE"
