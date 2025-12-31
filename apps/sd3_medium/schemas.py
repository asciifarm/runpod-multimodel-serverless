from pydantic import BaseModel, Field
from typing import Optional

class Input(BaseModel):
    prompt: str = Field(..., description="Prompt testuale")
    negative_prompt: Optional[str] = Field("", description="Negative prompt")
    steps: int = Field(28, ge=1, le=80)
    guidance_scale: float = Field(6.5, ge=0.0, le=20.0)
    width: int = Field(1024, ge=256, le=2048)
    height: int = Field(1024, ge=256, le=2048)
    seed: Optional[int] = Field(None)
