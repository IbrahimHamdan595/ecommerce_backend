from pydantic import BaseModel, Field
from typing import Optional, List

class ProductCreate(BaseModel):
    title: str
    slug: str
    description: Optional[str] = None
    price: float
    stock: int
    category_id: str
    images: List[str] = Field(default_factory=list)   # FIXED

class ProductOut(BaseModel):
    id: str
    title: str
    slug: str
    description: Optional[str] = None
    price: float
    stock: int
    category_id: str
    images: List[str] = Field(default_factory=list)   # FIXED
    is_active: bool

    class Config:
        orm_mode = True
        populate_by_name = True
