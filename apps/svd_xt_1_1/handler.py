
import torch
import base64
from io import BytesIO
from PIL import Image
import imageio
from diffusers import StableVideoDiffusionPipeline

pipe = None

def load():
    global pipe
    if pipe is None:
        pipe = StableVideoDiffusionPipeline.from_pretrained(
            "stabilityai/stable-video-diffusion-img2vid-xt-1-1",
            torch_dtype=torch.float16,
            variant="fp16"
        ).to("cuda")
        pipe.enable_attention_slicing()
    return pipe

def handler(event):
    data = event.get("input", {})
    image_b64 = data.get("image_base64")
    if not image_b64:
        return {"error": "image_base64 missing"}

    img = Image.open(BytesIO(base64.b64decode(image_b64))).convert("RGB")
    p = load()
    out = p(image=img)
    frames = out.frames[0]

    buf = BytesIO()
    imageio.mimsave(buf, frames, format="mp4", fps=7)
    return {"video": base64.b64encode(buf.getvalue()).decode()}
