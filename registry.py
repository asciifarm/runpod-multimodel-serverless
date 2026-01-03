MODEL_REGISTRY = {
    "sd15": {
        "task": "text_to_image",
        "model_id": "runwayml/stable-diffusion-v1-5",
        "loader": "text_to_image"
    },
    "sdxl": {
        "task": "text_to_image",
        "model_id": "stabilityai/stable-diffusion-xl-base-1.0",
        "loader": "text_to_image"
    },
    "svd": {
        "task": "image_to_video",
        "model_id": "stabilityai/stable-video-diffusion-img2vid",
        "loader": "image_to_video"
    }
}

MODEL_CACHE = {}
