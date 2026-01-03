import torch
from utils.image import base64_to_image, image_to_base64

def execute(pipe, input_data):
    image = base64_to_image(input_data["image_base64"])

    with torch.inference_mode():
        frames = pipe(
            image,
            num_frames=input_data.get("frames", 14),
            motion_bucket_id=int(input_data.get("motion_strength", 0.6) * 255)
        ).frames

    return {
        "type": "video",
        "frames": [image_to_base64(f) for f in frames]
    }
