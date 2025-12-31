import base64
from io import BytesIO
from PIL import Image

def image_to_base64_png(image: Image.Image) -> str:
    buf = BytesIO()
    image.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")

def base64_to_pil_image(b64: str) -> Image.Image:
    raw = base64.b64decode(b64)
    return Image.open(BytesIO(raw)).convert("RGB")
