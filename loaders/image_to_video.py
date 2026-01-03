import torch
from diffusers import StableVideoDiffusionPipeline

def load(model_id: str):
    pipe = StableVideoDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float16
    ).to("cuda")

    pipe.enable_attention_slicing()
    return pipe
