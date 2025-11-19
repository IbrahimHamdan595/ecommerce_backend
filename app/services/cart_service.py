from datetime import datetime
from typing import Optional, List

from bson import ObjectId

import app.core.database as database
from app.models.cart_model import CartModel, CartItemModel
from app.services.product_service import get_product_by_id

def get_cart_collection():
	if database.db is None:
		raise Exception("Database is not initialized yet")
	return database.db["carts"]

async def get_active_cart_for_user(user_id: str) -> Optional[CartModel]:
	collection = get_cart_collection()
	doc = await collection.find_one({
		"user_id": ObjectId(user_id),
		"is_active": True
	})
	return CartModel(**doc) if doc else None

async def create_cart_for_user(user_id: str) -> CartModel:
	collection = get_cart_collection()
	cart = CartModel(
		user_id=ObjectId(user_id),
		items=[]
	)
	await collection.insert_one(cart.model_dump(by_alias=True))
	return cart

async def get_or_create_cart(user_id: str) -> CartModel:
	cart = await get_active_cart_for_user(user_id)
	if cart:
		return cart
	return await create_cart_for_user(user_id)

async def add_item_to_cart(user_id: str, product_id: str, quantity: int) -> CartModel:
	cart = await get_or_create_cart(user_id)
	collection = get_cart_collection()

	product = await get_product_by_id(product_id)
	if not product:
		raise ValueError("Product not found")

	found = False
	for item in cart.items:
		if str(item.product_id) == product_id:
			item.quantity += quantity
			found = True
			break

	if not found:
		cart.items.append(
			CartItemModel(
				product_id=ObjectId(product_id),
                quantity=quantity,
                unit_price=product.price,
                title=product.title,
                image=(product.images[0] if getattr(product, "images", []) else None),
			)
		)

	cart.updated_at = datetime.utcnow()

	await collection.update_one(
		{"_id": cart.id},
		{"$set": {
			"items": [i.model_dump(by_alias=False) for i in cart.items],
			"update_at": cart.updated_at
		}}
	)

	return cart

async def update_cart_item(user_id: str, product_id: str, quantity: int) -> CartModel:
	cart = await get_or_create_cart(user_id)
	collection = get_cart_collection()

	updated_items: List[CartItemModel] = []
	for item in cart.items:
		if str(item.product_id) == product_id:
			if quantity <= 0:
				continue
			item.quantity = quantity
		updated_items.append(item)

	cart.items = updated_items
	cart.updated_at = datetime.utcnow()

	await collection.update_one(
		{"id": cart.id},
		{"$set": {
			"items": [i.model_dump(by_alias=False) for i in cart.items],
			"updated_at": cart.updated_at
		}}
	)

	return cart

async def remove_cart_item(user_id: str, product_id: str) -> CartModel:
	cart = await get_or_create_cart(user_id)
	collection = get_cart_collection()

	cart.items = [i for i in cart.items if str(i.product_id) != product_id]
	cart.updated_at = datetime.utcnow()

	await collection.update_one(
		{"id": cart.id},
		{"$set":  {
			"items": [i.model_dump(by_alias=False) for i in cart.items],
			"updated_at": cart.updated_at
		}}
	)

	return cart

async def clear_cart(user_id: str) -> CartModel:
	cart = await get_or_create_cart(user_id)
	collection = get_cart_collection()

	cart.items = []
	cart.updated_at = datetime.utcnow()

	await collection.update_one(
		{"id": cart.id},
		{"$set": {
			"items": [],
			"updated_at": cart.updated_at
		}}
	)

	return cart

def compute_cart_total(cart: CartModel) -> float:
	return sum(item.unit_price * item.quantity for item in cart.items)