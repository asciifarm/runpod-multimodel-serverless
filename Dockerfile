
FROM runpod/pytorch:1.0.2-cu1281-torch280-ubuntu2404

ENV HF_HOME=/workspace/.cache/huggingface \
    TRANSFORMERS_CACHE=/workspace/.cache/huggingface/transformers \
    DIFFUSERS_CACHE=/workspace/.cache/huggingface/diffusers \
    PIP_CACHE_DIR=/workspace/.cache/pip

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends git ffmpeg && \
    rm -rf /var/lib/apt/lists/*

COPY . /app

RUN python -m pip install -U pip && \
    python -m pip install -r requirements.txt

CMD ["bash", "scripts/runtime_bootstrap.sh"]
