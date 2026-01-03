import torch
from utils.image import image_to_base64

def execute(pipe, input_data):
    with torch.inference_mode():
        image = pipe(
            input_data["prompt"],
            num_inference_steps=input_data.get("steps", 25),
            guidance_scale=input_data.get("guidance", 7.5)
        ).images[0]

    return {
        "type": "image",
        "image": image_to_base64(image)
    }
