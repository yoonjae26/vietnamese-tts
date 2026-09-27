# Dùng chung cho các script tạo môi trường. Mã nguồn các model được clone vào $ENGINES_DIR.
set -euo pipefail
CONDA="${CONDA:-$HOME/miniconda3/bin/conda}"
ENGINES_DIR="${ENGINES_DIR:-$HOME/vitts-engines}"
mkdir -p "$ENGINES_DIR"

make_env() {  # make_env <tên> <phiên bản python>
  if [ ! -x "$HOME/miniconda3/envs/$1/bin/python" ]; then
    "$CONDA" create -y -q -n "$1" "python=$2"
  fi
  PY="$HOME/miniconda3/envs/$1/bin/python"
  PIP="$PY -m pip"
}

clone() {  # clone <github user/repo> <commit hoặc nhánh>
  local dir="$ENGINES_DIR/$(basename "$1")"
  [ -d "$dir" ] || git clone -q "https://github.com/$1" "$dir"
  git -C "$dir" fetch -q --depth 1 origin "$2" 2>/dev/null || true
  git -C "$dir" checkout -q "$2"
  echo "$dir"
}
