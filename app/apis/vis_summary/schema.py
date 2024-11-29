from pydantic import BaseModel
from typing import List, Dict

class VISSUMMARYResponseSchema(BaseModel):
    text: str