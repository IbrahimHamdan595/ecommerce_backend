from fastapi import APIRouter, HTTPException
from app.schemas.product_schema import ProductCreate, ProductOut
from app.services.product_service import *

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductOut)
async def create(data:ProductCreate):
	product = await create_product(data)
	return ProductOut(
		id=str(product.id),
        title=product.title,
        slug=product.slug,
        description=product.description,
        price=product.price,
        stock=product.stock,
        category_id=str(product.category_id),
        images=product.images,
        is_active=product.is_active
	)

@router.get("/", response_model=list[ProductOut])
async def get_all():
	products = await list_product()
	return [
		ProductOut(
            id=str(p.id),
            title=p.title,
            slug=p.slug,
            description=p.description,
            price=p.price,
            stock=p.stock,
            category_id=str(p.category_id),
            images=p.images,
            is_active=p.is_active
        )
        for p in products
	]

# update product
@router.put("/{product_id}")
async def update(product_id: str, data: ProductCreate):
    ok = await update_product(product_id, data.dict(exclude_none=True))

    if not ok:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Product updated successfully"}

# delete product
@router.delete("/{product_id}")
async def delete(product_id: str):
    ok = await delete_product(product_id)

    if not ok:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Product deleted successfully"}

@router.get("/search")
async def search_products(
    page: int = 1,
    limit: int = 10,
    search: str | None = None,
    category: str | None = None,
    sort: str | None = None
):
    result = await query_products(page, limit, search, category, sort)

    return {
        "items": [
            ProductOut(
                id=str(p.id),
                title=p.title,
                slug=p.slug,
                description=p.description,
                price=p.price,
                stock=p.stock,
                category_id=str(p.category_id),
                images=p.images,
                is_active=p.is_active,
            )
            for p in result["items"]
        ],
        "total": result["total"],
        "page": result["page"],
        "limit": result["limit"]
    }

@router.get("/{product_id}", response_model=ProductOut)
async def get_by_id(product_id: str):
    product = await get_product_by_id(product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return ProductOut(
        id=str(product.id),
        title=product.title,
        slug=product.slug,
        description=product.description,
        price=product.price,
        stock=product.stock,
        category_id=str(product.category_id),
        images=product.images,
        is_active=product.is_active
    )

@router.get("/slug/{slug}", response_model=ProductOut)
async def get_by_slug(slug: str):
    product = await get_product_by_slug(slug)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return ProductOut(
        id=str(product.id),
        title=product.title,
        slug=product.slug,
        description=product.description,
        price=product.price,
        stock=product.stock,
        category_id=str(product.category_id),
        images=product.images,
        is_active=product.is_active
    )

@router.put("/{product_id}/toggle")
async def toggle(product_id: str, state: bool):
    ok = await toggle_product(product_id, state)

    if not ok:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Product state updated", "active": state}

