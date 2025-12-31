
#!/usr/bin/env bash
set -euo pipefail

WORKER="${WORKER:-sd3_medium}"

export HF_HOME=${HF_HOME:-/workspace/.cache/huggingface}
export TRANSFORMERS_CACHE=${TRANSFORMERS_CACHE:-$HF_HOME/transformers}
export DIFFUSERS_CACHE=${DIFFUSERS_CACHE:-$HF_HOME/diffusers}
export PIP_CACHE_DIR=${PIP_CACHE_DIR:-/workspace/.cache/pip}

echo "Starting worker: $WORKER"

pip install -r "apps/$WORKER/requirements.txt"
python "apps/$WORKER/download_weights.py" || true

exec python -u handler.py
