import torch
from diffusers import StableDiffusionPipeline

def load(model_id: str):
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float16
    ).to("cuda")

    pipe.enable_attention_slicing()
    pipe.safety_checker = None
    return pipe
