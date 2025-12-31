#!/usr/bin/env bash
set -euo pipefail

: "${WORKER:=sd3-medium}"
: "${REPO_URL:=}"
: "${REPO_REF:=main}"

# RunPod best practice: cache su volume
export HF_HOME="${HF_HOME:-/workspace/.cache/huggingface}"
export TRANSFORMERS_CACHE="${TRANSFORMERS_CACHE:-$HF_HOME/transformers}"
export DIFFUSERS_CACHE="${DIFFUSERS_CACHE:-$HF_HOME/diffusers}"
export PIP_CACHE_DIR="${PIP_CACHE_DIR:-/workspace/.cache/pip}"

WORKDIR="/app"
mkdir -p "$WORKDIR"
cd "$WORKDIR"

if [[ -n "$REPO_URL" ]]; then
  echo "Cloning repo $REPO_URL ($REPO_REF) ..."
  rm -rf repo || true
  git clone --depth 1 --branch "$REPO_REF" "$REPO_URL" repo
  cd repo
else
  # Se la repo è già nel filesystem (es. mount), usa quella
  cd /app/repo 2>/dev/null || true
fi

APP_DIR="apps/$WORKER"
if [[ ! -d "$APP_DIR" ]]; then
  echo "Worker '$WORKER' non trovato in $APP_DIR"
  exit 1
fi

python -m pip install --upgrade pip

# Install minimo per worker (niente monorepo requirements globali)
python -m pip install -r "$APP_DIR/requirements.txt"

# Warmup/cache pesi (idempotente)
python "$APP_DIR/download_weights.py" || true

# Avvio handler
exec python -u "$APP_DIR/handler.py"
