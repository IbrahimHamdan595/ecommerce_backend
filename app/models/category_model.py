from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, validator
from bson import ObjectId

from app.models.user_model import PyObjectId

class CategoryModel(BaseModel):
	id: Optional[str] = Field(default=None, alias="_id")
	name: str
	slug: str
	description: Optional[str] = None
	image: Optional[str] = None
	is_active: bool = True
	created_at: datetime = Field(default_factory=datetime.utcnow)

	# ⭐ Convert ObjectId → str BEFORE Pydantic validates
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