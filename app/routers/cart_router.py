from fastapi import APIRouter, Depends, HTTPException

from app.schemas.cart_schema import CartItemIn, CartItemOut, CartItemUpdate, CartOut
from app.services.cart_service import *
from app.routers.auth_router import get_current_user
from app.schemas.user_schema import UserOut

router = APIRouter(prefix="/cart", tags=["Cart"])

# 🔹 Helper: convert CartModel -> CartOuto_cart_out(cart, user_id: str) -> CartOut:
def to_cart_out(cart, user_id: str) -> CartOut:
	items_out = [
		CartItemOut(
			product_id=str(item.product_id),
            title=item.title,
            image=item.image,
            quantity=item.quantity,
            unit_price=item.unit_price,
            subtotal=item.unit_price * item.quantity,
		)
		for item in cart.items
	]

	return CartOut(
		id=str(cart.id),
		user_id=user_id,
		items=items_out,
		total=compute_cart_total(cart),
		is_active=cart.is_active,
		created_at=cart.created_at,
		updated_at=cart.updated_at
	)

# 🧾 Get current user's cart
@router.get("", response_model=CartOut)
async def get_my_cart(user=Depends(get_current_user)):
	cart = await get_or_create_cart(str(user.id))
	return to_cart_out(cart, str(user.id))

# ➕ Add item
@router.post("/items", response_model=CartOut)
async def add_item(body: CartItemIn, user=Depends(get_current_user)):
	try:
		cart =await add_item_to_cart(str(user.id), body.product_id, body.quantity)
	except ValueError as e:
		raise HTTPException(status_code=404, detail=str(e))
	return to_cart_out(cart, str(user.id))

# ✏️ Update quantity
@router.patch("/items/{product_id}", response_model=CartOut)
async def delete_item(product_id: str, user=Depends(get_current_user)):
	cart = await remove_cart_item(str(user.id), product_id)
	return to_cart_out(cart, str(user.id))

# 🗑 Remove one item
@router.delete("/items/{product_id}", response_model=CartOut)
async def delete_item(product_id: str, user=Depends(get_current_user)):
	cart = await remove_cart_item(str(user.id), product_id)
	return to_cart_out(cart, str(user.id))

# 🧹 Clear cart
@router.delete("", response_model=CartOut)
async def clear_my_cart(user=Depends(get_current_user)):
	cart = await clear_cart(str(user.id))
	return to_cart_out(cart, str(user.id))