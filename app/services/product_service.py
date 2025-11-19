import app.core.database as database
from app.models.product_model import ProductModel
from bson import ObjectId
from typing import List, Optional
from app.schemas.product_schema import ProductCreate

def get_product_collection():
	return database.db['products']

async def create_product(data: ProductCreate):
    col = get_product_collection()

    # Convert category_id to ObjectId
    doc = data.dict()
    doc["category_id"] = ObjectId(doc["category_id"])

    # REMOVE id if exists
    if "_id" in doc:
        del doc["_id"]

    # Insert & get the generated ID
    result = await col.insert_one(doc)

    # Create a clean ProductModel
    product = ProductModel(
        id=str(result.inserted_id),
        **data.dict()
    )

    return product


async def list_product():
	cursor = get_product_collection().find({})
	return [ProductModel(**doc) for doc in await cursor.to_list(None)]

async def update_product(product_id: str, data: dict):
    collection = get_product_collection()

    # convert category_id if exists
    if "category_id" in data:
        data["category_id"] = ObjectId(data["category_id"])

    result = await collection.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": data}
    )
    return result.modified_count > 0


async def delete_product(product_id: str):
    collection = get_product_collection()
    result = await collection.delete_one({"_id": ObjectId(product_id)})
    return result.deleted_count > 0

async def query_products(
	page: int = 1,
    limit: int = 10,
    search: Optional[str] = None,
	category_id: Optional[str] = None,
    sort: Optional[str] = None
):
	collection = get_product_collection()
	skip = (page - 1) * limit

	query = {}

	# search filter
	if search:
		query["title"] = {"$regex": search, "$options": "i"}

	# Category filter
	if category_id:
		query["category_id"] = ObjectId(category_id)

	# Sorting
	sort_option = None
	if sort == "price_asc":
		sort_option = [("price", 1)]
	elif sort == "price_desc":
		sort_option = [("price", -1)]
	elif sort == "newest":
		sort_option = [("created_at", -1)]
	elif sort == "stock":
		sort_option = [("stock", -1)]

	cursor = (
		collection.find(query)
		.sort(sort_option or [("_id", -1)])
		.skip(skip)
		.limit(limit)
	)

	items = [ProductModel(**doc) for doc in await cursor.to_list(limit)]
	total_count = await collection.count_documents(query)

	return {
		"items": items,
		"total": total_count,
		"page": page,
		"limit": limit
	}

async def get_product_by_id(product_id: str):
	doc = await get_product_collection().find_one({"_id": ObjectId(product_id)})
	return ProductModel(**doc) if doc else None

async def get_product_by_slug(slug: str):
	doc = await get_product_collection().find_one({"slug": slug})
	return ProductModel(**doc) if doc else None

async def toggle_product(product_id: str, state: bool):
	result = await get_product_collection().update_one(
	    {"_id": ObjectId(product_id)},
        {"$set": {"is_active": state}}
	)
	return result.modified_count > 0