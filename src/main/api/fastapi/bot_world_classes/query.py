from pydantic import BaseModel
from typing import Optional


"""
Input to get recommendation
"""
class Query(BaseModel):
    user_id: str
    top_k: int
    chat_id: Optional[int] = None