
import os
import importlib
import runpod

WORKER = os.environ.get("WORKER", "sd3_medium")

def handler(event):
    module = importlib.import_module(f"apps.{WORKER}.handler")
    return module.handler(event)

runpod.serverless.start({"handler": handler})
