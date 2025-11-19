from datetime import datetime
from typing import Optional, Any
from bson import ObjectId

from pydantic import BaseModel, EmailStr, Field, ConfigDict, GetCoreSchemaHandler
from pydantic_core import core_schema
from pydantic.json_schema import JsonSchemaValue

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler: GetCoreSchemaHandler):
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema()
        )

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v  # ← RETURN the actual ObjectId, not cls(v)
        if isinstance(v, str) and ObjectId.is_valid(v):
            return ObjectId(v)  # ← return valid ObjectId
        raise ValueError("Invalid ObjectId")

    @classmethod
    def __get_pydantic_json_schema__(cls, schema, handler) -> JsonSchemaValue:
        json_schema = handler(schema)
        json_schema.update(type="string")
        return json_schema

class UserModel(BaseModel):
	id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias = "_id")
	full_name: str
	email: EmailStr
	phone: Optional[str] = None
	password_hash: str
	role: str = "customer"
	is_verified: bool = False
	created_at: datetime = Field(default_factory = datetime.utcnow)

	model_config = ConfigDict(
		arbitrary_types_allowed = True,
		populate_by_name = True,
		json_encoders = {ObjectId: str}
	)