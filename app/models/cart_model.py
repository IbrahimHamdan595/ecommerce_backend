from datetime import datetime
from typing import Optional, Any, List
from bson import ObjectId

from pydantic import BaseModel, Field, ConfigDict, GetCoreSchemaHandler, validator
from pydantic_core import core_schema
from pydantic.json_schema import JsonSchemaValue


class CartItemModel(BaseModel):
    product_id: str
    quantity: int = 1
    unit_prices: float
    title: str
    image: Optional[str] = None

    @validator("product_id", pre=True)
    def convert_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

class CartModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    items: List[CartItemModel] = Field(default_factory=list)
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @validator("id", pre=True)
    def convert_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )