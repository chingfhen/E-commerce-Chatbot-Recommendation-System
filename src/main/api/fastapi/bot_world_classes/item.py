from pydantic import BaseModel
from typing import Optional

"""
A Product Recommendation
"""
class Product(BaseModel):
    product_id: int
    product_name: str
    categories: str
    image_url: str