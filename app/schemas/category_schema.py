from pydantic import BaseModel
from typing import Optional

class CategoryCreate(BaseModel):
	name: str
	slug: str
	description: Optional[str] = None
	image: Optional[str] = None

class CategoryOut(BaseModel):
	id: str
	name: str
	slug: str
	description: Optional[str]
	image: Optional[str]
	is_active: bool