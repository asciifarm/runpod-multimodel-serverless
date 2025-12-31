
FROM runpod/pytorch:1.0.2-cu1281-torch280-ubuntu2404

ENV HF_HOME=/workspace/.cache/huggingface \
    TRANSFORMERS_CACHE=/workspace/.cache/huggingface/transformers \
    DIFFUSERS_CACHE=/workspace/.cache/huggingface/diffusers

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

CMD ["python","-u","handler.py"]
