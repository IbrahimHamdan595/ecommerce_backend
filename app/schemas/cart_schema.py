from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, EmailStr

class CartItemIn(BaseModel):
	product_id: str
	quantity: int = 1

class CartItemUpdate(BaseModel):
	quantity: int

class CartItemOut(BaseModel):
	product_id: str
	title: str
	image: Optional[str] = None
	quantity: int
	unit_price: float
	subtotal: float

class CartOut(BaseModel):
	id: str
	user_id: str
	items: List[CartItemOut]
	total: float
	is_active: bool
	created_at: datetime
	updated_at: datetime

	model_config = ConfigDict(from_attributes=True)