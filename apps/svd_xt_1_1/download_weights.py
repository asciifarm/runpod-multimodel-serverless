import os
from huggingface_hub import snapshot_download

MODEL_ID = "stabilityai/stable-video-diffusion-img2vid-xt-1-1"

def main():
    cache_dir = os.environ.get("DIFFUSERS_CACHE") or os.environ.get("HF_HOME")
    snapshot_download(
        repo_id=MODEL_ID,
        cache_dir=cache_dir,
        local_files_only=False,
        resume_download=True,
    )
    print(f"Cached: {MODEL_ID}")

if __name__ == "__main__":
    main()
