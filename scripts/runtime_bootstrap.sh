#!/usr/bin/env bash
set -euo pipefail

# ====== Config ======
WORKER="${WORKER:-sd3_medium}"
REPO_URL="${REPO_URL:?REPO_URL env var is required}"
REPO_REF="${REPO_REF:-main}"

APP_ROOT="/app"
REPO_DIR="$APP_ROOT/repo"

# ====== Cache paths (volume) ======
export HF_HOME="${HF_HOME:-/workspace/.cache/huggingface}"
export TRANSFORMERS_CACHE="${TRANSFORMERS_CACHE:-$HF_HOME/transformers}"
export DIFFUSERS_CACHE="${DIFFUSERS_CACHE:-$HF_HOME/diffusers}"
export PIP_CACHE_DIR="${PIP_CACHE_DIR:-/workspace/.cache/pip}"

echo "[STEP] Worker       : $WORKER"
echo "[STEP] Repo URL     : $REPO_URL"
echo "[STEP] Repo branch  : $REPO_REF"
echo "[STEP] Repo dir     : $REPO_DIR"

mkdir -p "$APP_ROOT"
cd "$APP_ROOT"

# ====== Clone repo if missing ======
if [ ! -d "$REPO_DIR/.git" ]; then
  echo "[STEP] Cloning repository..."
  rm -rf "$REPO_DIR"
  git clone --depth 1 --branch "$REPO_REF" "$REPO_URL" repo
else
  echo "[STEP] Repository already present, skipping clone"
fi

cd "$REPO_DIR"

# ====== Validate worker ======
if [ ! -d "apps/$WORKER" ]; then
  echo "[ERROR] Worker '$WORKER' not found in apps/"
  ls -la apps
  exit 1
fi

# ====== Install deps (worker-only) ======
echo "[STEP] Installing dependencies for $WORKER"
pip install --no-cache-dir -r "apps/$WORKER/requirements.txt"

# ====== Warmup model weights (idempotent) ======
echo "[STEP] Warming up model cache (if needed)"
python "apps/$WORKER/download_weights.py" || true

# ====== Start RunPod handler ======
echo "[STEP] Starting RunPod serverless handler"
exec python -u handler.py
