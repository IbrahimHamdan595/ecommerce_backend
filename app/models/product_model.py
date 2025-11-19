from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict, validator
from bson import ObjectId


class ProductModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    title: str
    slug: str
    description: Optional[str] = None
    price: float
    stock: int = 0
    category_id: Optional[str] = Field(alias="category_id")
    images: List[str] = Field(default_factory=list)
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @validator("id", "category_id", pre=True)
    def convert_objectid(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )
