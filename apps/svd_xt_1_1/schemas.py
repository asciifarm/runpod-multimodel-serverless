from pydantic import BaseModel, Field
from typing import Optional

class Input(BaseModel):
    image_base64: str = Field(..., description="Immagine input base64 (png/jpg)")
    motion_bucket_id: int = Field(127, ge=1, le=255)
    noise_aug_strength: float = Field(0.02, ge=0.0, le=1.0)
    fps: int = Field(7, ge=1, le=30)
