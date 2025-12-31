import os
import runpod
import torch
from diffusers import StableDiffusion3Pipeline
from common.b64 import image_to_base64_png
from .schemas import Input

MODEL_ID = "stabilityai/stable-diffusion-3-medium"
TORCH_DTYPE = torch.float16

# Global pipeline (lazy loaded)
pipe = None

def load():
    global pipe
    if pipe is not None:
        return pipe

    assert torch.cuda.is_available(), "CUDA non disponibile: serve GPU"

    # Usa cache su volume (/workspace) se configurata
    pipe = StableDiffusion3Pipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=TORCH_DTYPE,
    ).to("cuda")

    # Ottimizzazioni safe per ridurre memoria e migliorare cold-start
    pipe.enable_attention_slicing()

    return pipe

def handler(event):
    global pipe
    data = event.get("input", {}) or {}
    try:
        inp = Input(**data)
    except Exception as e:
        return {"error": f"invalid_input: {e}"}

    p = load()

    generator = None
    if inp.seed is not None:
        generator = torch.Generator(device="cuda").manual_seed(int(inp.seed))

    out = p(
        prompt=inp.prompt,
        negative_prompt=inp.negative_prompt,
        num_inference_steps=inp.steps,
        guidance_scale=inp.guidance_scale,
        width=inp.width,
        height=inp.height,
        generator=generator,
    )

    image = out.images[0]
    return {
        "model": MODEL_ID,
        "image": image_to_base64_png(image),
    }

runpod.serverless.start({"handler": handler})
