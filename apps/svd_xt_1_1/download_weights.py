
from huggingface_hub import snapshot_download

MODEL_ID = "stabilityai/stable-video-diffusion-img2vid-xt-1-1"

snapshot_download(repo_id=MODEL_ID, resume_download=True)
