from datetime import datetime
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict, validator

class AddressModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")  # MongoDB _id → string
    user_id: str

    full_name: str
    phone: str
    country: str
    city: str
    street: str
    building: Optional[str] = None
    floor: Optional[int] = None
    additional_info: Optional[str] = None

    is_default: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # ⭐ Convert ObjectId → str BEFORE Pydantic validates
    @validator("id", pre=True)
    def convert_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )
