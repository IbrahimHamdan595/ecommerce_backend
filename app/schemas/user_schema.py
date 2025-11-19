from pydantic import BaseModel, EmailStr, ConfigDict

# Input schemas
class RegisterSchema(BaseModel):
	full_name: str
	email: EmailStr
	phone: str | None = None
	password: str

class LoginSchema(BaseModel):
	email: EmailStr
	password: str

# Output Schemas
class UserOut(BaseModel):
	id: str
	full_name: str
	email: EmailStr
	phone: str | None
	role: str
	is_verified: bool

	model_config = ConfigDict(from_attributes=True)