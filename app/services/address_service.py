import app.core.database as database
from app.models.address_model import AddressModel
from app.models.user_model import PyObjectId

def get_address_collection():
	if database.db is None:
		raise Exception("Database is not initialized yet")
	return database.db["addresses"]

async def create_address(user_id: str, data):
    col = get_address_collection()

    # Remove previous defaults
    if data.is_default:
        await col.update_many(
            {"user_id": user_id},
            {"$set": {"is_default": False}}
        )

    # Create model (id=None)
    address = AddressModel(
        user_id=user_id,
        **data.model_dump()
    )

    # EXCLUDE _id/id so MongoDB can generate it
    doc = address.model_dump(by_alias=True, exclude={"id", "_id"})

    result = await col.insert_one(doc)

    address.id = str(result.inserted_id)
    return address

# List all addresses of the user
async def list_addresses(user_id: str):
	col = get_address_collection()
	cursor = col.find({"user_id": user_id})
	return [AddressModel(**a) async for a in cursor]

# Update an address
async def update_address(address_id: str, user_id: str, data):
	col = get_address_collection()

	update_data = {k:v for k, v in data.model_dump().items() if v is not None}

	if "is_default" in update_data and update_data["is_default"]:
		await col.update_many(
			{"user_id": user_id},
			{"$set": {"is_default": False}}
		)

	await col.update_one(
		{"_id": PyObjectId(address_id), "user_id": user_id},
		{"$set": update_data}
	)

	doc = await col.find_one({"_id": PyObjectId(address_id)})
	return AddressModel(**doc) if doc else None

# Delete an address
async def delete_address(address_id: str, user_id: str):
	col = get_address_collection()
	result = await col.delete_one(
		{"_id": PyObjectId(address_id), "user_id": user_id}
	)
	return result.deleted_count == 1
