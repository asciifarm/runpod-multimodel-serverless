
from huggingface_hub import snapshot_download

MODEL_ID = "stabilityai/stable-diffusion-3-medium"

snapshot_download(repo_id=MODEL_ID, resume_download=True)
