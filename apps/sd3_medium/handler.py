
import torch
from diffusers import StableDiffusion3Pipeline
from io import BytesIO
import base64
from PIL import Image

pipe = None

def image_to_base64(img: Image.Image):
    buf = BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()

def load():
    global pipe
    if pipe is None:
        pipe = StableDiffusion3Pipeline.from_pretrained(
            "stabilityai/stable-diffusion-3-medium",
            torch_dtype=torch.float16
        ).to("cuda")
        pipe.enable_attention_slicing()
    return pipe

def handler(event):
    data = event.get("input", {})
    prompt = data.get("prompt")
    if not prompt:
        return {"error": "prompt missing"}

    p = load()
    img = p(prompt=prompt, num_inference_steps=data.get("steps", 28)).images[0]
    return {"image": image_to_base64(img)}
