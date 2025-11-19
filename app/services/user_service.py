from bson import ObjectId

import app.core.database as database
from app.models.user_model import UserModel
from app.utils.hashing import hash_password, verify_password
from app.schemas.user_schema import RegisterSchema

def get_users_collection():
	if database.db is None:
		raise Exception("Database is not initialized yet")
	return database.db["users"]

async def create_user(data):
	collection = get_users_collection()
	user = UserModel(
		full_name=data.full_name,
		email=data.email,
		phone=data.phone,
		password_hash=hash_password(data.password)
	)

	await collection.insert_one(user.model_dump(by_alias=True))
	return user

async def get_user_by_email(email:str):
	collection = get_users_collection()
	user = await collection.find_one({"email": email})
	if user:
		user["_id"] = str(user["_id"])  # force convert for debugging
		return UserModel(**user)
	return None

async def authenticate_user(email: str, password: str):
	user = await get_user_by_email(email)
	if not user:
		return None
	if not verify_password(password, user.password_hash):
		return None
	return user