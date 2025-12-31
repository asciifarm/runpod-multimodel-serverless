import base64
from io import BytesIO
import runpod
import torch
import imageio
from diffusers import StableVideoDiffusionPipeline
from common.b64 import base64_to_pil_image
from .schemas import Input

MODEL_ID = "stabilityai/stable-video-diffusion-img2vid-xt-1-1"
TORCH_DTYPE = torch.float16

pipe = None

def load():
    global pipe
    if pipe is not None:
        return pipe

    assert torch.cuda.is_available(), "CUDA non disponibile: serve GPU"

    pipe = StableVideoDiffusionPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=TORCH_DTYPE,
        variant="fp16",
    ).to("cuda")

    pipe.enable_attention_slicing()
    return pipe

def frames_to_mp4_base64(frames, fps: int) -> str:
    # frames: list of HxWx3 uint8
    buf = BytesIO()
    imageio.mimsave(buf, frames, format="mp4", fps=fps)
    return base64.b64encode(buf.getvalue()).decode("utf-8")

def handler(event):
    data = event.get("input", {}) or {}
    try:
        inp = Input(**data)
    except Exception as e:
        return {"error": f"invalid_input: {e}"}

    p = load()

    init_image = base64_to_pil_image(inp.image_base64)

    out = p(
        image=init_image,
        motion_bucket_id=inp.motion_bucket_id,
        noise_aug_strength=inp.noise_aug_strength,
    )

    # Diffusers returns frames as list batches; we take first sample
    frames = out.frames[0]
    return {
        "model": MODEL_ID,
        "video_mp4_base64": frames_to_mp4_base64(frames, fps=inp.fps),
        "fps": inp.fps
    }

runpod.serverless.start({"handler": handler})
