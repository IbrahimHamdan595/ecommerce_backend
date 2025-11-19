from pydantic import BaseModel, Field
from typing import Optional

class AddressCreate(BaseModel):
	full_name: str
	phone: str
	country: str
	city: str
	street: str
	building: Optional[str] | None = None
	floor: Optional[int] | None = None
	additional_info: Optional[str] | None = None
	is_default: bool = False

class AddressUpdate(BaseModel):
	full_name: Optional[str] = None
	phone: Optional[str] = None
	country: Optional[str] = None
	city: Optional[str] = None
	street: Optional[str] = None
	building: Optional[str] = None
	floor: Optional[int] = None
	additional_info: Optional[str] = None
	is_default: Optional[bool] = None

class AddressOut(BaseModel):
	id: str = Field(alias="_id")
	full_name: str
	phone: str
	country: str
	city: str
	street: str
	building: Optional[str]
	floor: Optional[int]
	additional_info: Optional[str]
	is_default: bool

	class Config:
		populate_by_name = True
		orm_mode = True