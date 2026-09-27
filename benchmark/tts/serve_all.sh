#!/usr/bin/env bash
# Bật một worker cho mỗi model (mỗi worker trong môi trường conda riêng) và gateway tương thích OpenAI.
#
#   bash benchmark/tts/serve_all.sh                  # tất cả model, gateway ở :8000
#   bash benchmark/tts/serve_all.sh f5 vieneu        # chỉ vài model
#
# Ctrl+C tắt cả gateway và các worker. Chỉ dùng GPU 0 (máy dùng chung).
set -uo pipefail
export CUDA_VISIBLE_DEVICES=0
export COQUI_TOS_AGREED=1
cd "$(dirname "$0")/../.."

ENVS="$HOME/miniconda3/envs"
LOGS=outputs/logs
GATEWAY_PORT="${GATEWAY_PORT:-8000}"
mkdir -p "$LOGS"

declare -A ENV_OF=(
  [mms]=vitts-coqui [vixtts]=vitts-coqui [piper]=vitts-coqui [f5]=vitts-f5
  [vieneu]=vitts-vieneu [viettts]=vitts-viettts [indextts2]=vitts-indextts
)
declare -A PORT_OF=(
  [mms]=9101 [vixtts]=9102 [f5]=9103 [vieneu]=9104 [viettts]=9105 [indextts2]=9106 [piper]=9107
)
# Mặc định: VieNeu trước (giấy phép Apache-2.0, cân bằng nhất trong benchmark)
ENGINES=(${@:-vieneu f5 indextts2 vixtts viettts mms piper})

PIDS=()
cleanup() { echo; echo "Tắt ${#PIDS[@]} tiến trình..."; kill "${PIDS[@]}" 2>/dev/null; wait; }
trap cleanup EXIT INT TERM

WORKERS=""
for e in "${ENGINES[@]}"; do
  extra=""; [ "$e" = piper ] && extra="--cpu"
  "$ENVS/${ENV_OF[$e]}/bin/python" benchmark/tts/worker.py --engine "$e" --port "${PORT_OF[$e]}" $extra \
    > "$LOGS/worker_$e.log" 2>&1 &
  PIDS+=($!)
  WORKERS+="$e=http://127.0.0.1:${PORT_OF[$e]},"
  echo "worker $e -> :${PORT_OF[$e]} (log: $LOGS/worker_$e.log)"
done

echo "Đợi các worker nạp model..."
for e in "${ENGINES[@]}"; do
  until grep -q "READY" "$LOGS/worker_$e.log" 2>/dev/null; do
    if ! kill -0 "${PIDS[@]}" 2>/dev/null && ! grep -q READY "$LOGS/worker_$e.log"; then
      grep -q Traceback "$LOGS/worker_$e.log" && { echo "worker $e lỗi, xem $LOGS/worker_$e.log"; break; }
    fi
    sleep 2
  done
  grep -q READY "$LOGS/worker_$e.log" && echo "  sẵn sàng: $e"
done

echo "Gateway: http://0.0.0.0:$GATEWAY_PORT (model mặc định: ${ENGINES[0]})"
"$ENVS/vitts-bench/bin/python" -m vitts.server --port "$GATEWAY_PORT" \
  --worker "${WORKERS%,}" --default-model "${ENGINES[0]}" &
PIDS+=($!)
wait "${PIDS[-1]}"
