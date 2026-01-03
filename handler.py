import runpod
from registry import MODEL_REGISTRY, MODEL_CACHE
from loaders import text_to_image, image_to_video
from executors import text_to_image as t2i_exec
from executors import image_to_video as i2v_exec

LOADER_MAP = {
    "text_to_image": text_to_image.load,
    "image_to_video": image_to_video.load
}

EXECUTOR_MAP = {
    "text_to_image": t2i_exec.execute,
    "image_to_video": i2v_exec.execute
}

def load_model(model_key):
    if model_key in MODEL_CACHE:
        return MODEL_CACHE[model_key]

    cfg = MODEL_REGISTRY[model_key]
    loader = LOADER_MAP[cfg["loader"]]
    model = loader(cfg["model_id"])

    MODEL_CACHE[model_key] = model
    return model

def handler(event):
    input_data = event.get("input", {})
    task = input_data.get("task")
    model_key = input_data.get("model")

    if not task or not model_key:
        return {"error": "task and model are required"}

    cfg = MODEL_REGISTRY.get(model_key)
    if not cfg or cfg["task"] != task:
        return {"error": "model not compatible with task"}

    pipe = load_model(model_key)
    executor = EXECUTOR_MAP[task]

    return executor(pipe, input_data)

runpod.serverless.start({"handler": handler})
