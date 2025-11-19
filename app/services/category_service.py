import app.core.database as database
from app.models.category_model import CategoryModel
from bson import ObjectId

def get_category_collection():
	return database.db['categories']

async def create_category(data):
	col = get_category_collection()
	category = CategoryModel(**data.dict())
	doc = category.model_dump(by_alias=True, exclude={"id", "_id"})
	result = await col.insert_one(doc)
	category.id = str(result.inserted_id)
	return category


async def list_categories():
	cursor = get_category_collection().find({})
	return [CategoryModel(**doc) for doc in await cursor.to_list(None)]

async def update_category(category_id: str, data: dict):
    collection = get_category_collection()
    result = await collection.update_one(
        {"_id": ObjectId(category_id)},
        {"$set": data}
    )
    return result.modified_count > 0

async def delete_category(category_id: str):
    collection = get_category_collection()
    result = await collection.delete_one({"_id": ObjectId(category_id)})
    return result.deleted_count > 0