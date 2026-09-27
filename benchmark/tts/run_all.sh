#!/usr/bin/env bash
# Sinh audio cho các model (mỗi model trong môi trường conda riêng) rồi chấm điểm.
#
#   bash benchmark/tts/run_all.sh                 # tất cả
#   bash benchmark/tts/run_all.sh vieneu viettts  # chỉ vài model
#
# Chỉ dùng GPU 0 (máy dùng chung). synthesize.py sẽ từ chối chạy nếu biến này khác "0".
export CUDA_VISIBLE_DEVICES=0
export COQUI_TOS_AGREED=1

cd "$(dirname "$0")/../.."
ENVS="$HOME/miniconda3/envs"
LOGS=outputs/logs
mkdir -p "$LOGS"

declare -A ENV_OF=(
  [mms]=vitts-coqui [vixtts]=vitts-coqui [piper]=vitts-coqui [f5]=vitts-f5
  [vieneu]=vitts-vieneu [viettts]=vitts-viettts [indextts2]=vitts-indextts
)
ENGINES=("${@:-mms vixtts f5 vieneu viettts indextts2 piper}")
ENGINES=(${ENGINES[@]})

for e in "${ENGINES[@]}"; do
  extra=""
  [ "$e" = piper ] && extra="--cpu"   # Piper được thiết kế cho CPU
  echo "[$(date +%T)] synth $e"
  if "$ENVS/${ENV_OF[$e]}/bin/python" benchmark/tts/synthesize.py --engine "$e" $extra > "$LOGS/synth_$e.log" 2>&1; then
    echo "[$(date +%T)] OK $e: $(tail -1 "$LOGS/synth_$e.log")"
  else
    echo "[$(date +%T)] FAIL $e (xem $LOGS/synth_$e.log)"
  fi
done

echo "[$(date +%T)] evaluate"
"$ENVS/vitts-coqui/bin/python" benchmark/tts/evaluate.py > "$LOGS/evaluate.log" 2>&1 \
  && echo "[$(date +%T)] OK evaluate" || echo "[$(date +%T)] FAIL evaluate (xem $LOGS/evaluate.log)"
