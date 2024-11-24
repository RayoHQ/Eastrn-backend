from pydantic import BaseModel
from typing import List, Dict

class SUMMARYResponseSchema(BaseModel):
    text: str