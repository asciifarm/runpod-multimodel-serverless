FROM runpod/pytorch:1.0.2-cu1281-torch280-ubuntu2404

ENV HF_HOME=/workspace/.cache/huggingface \
    TRANSFORMERS_CACHE=/workspace/.cache/huggingface/transformers \
    DIFFUSERS_CACHE=/workspace/.cache/huggingface/diffusers \
    PIP_CACHE_DIR=/workspace/.cache/pip

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends git ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Entrypoint minimale: clona repo a runtime
CMD ["bash", "-lc", "git clone --depth 1 https://github.com/<ORG>/<REPO>.git repo && cd repo && bash scripts/runtime_bootstrap.sh"]
