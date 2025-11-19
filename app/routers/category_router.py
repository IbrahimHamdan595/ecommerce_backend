from fastapi import APIRouter, HTTPException
from app.schemas.category_schema import CategoryCreate, CategoryOut
from app.services.category_service import (
     create_category, list_categories, update_category, delete_category
)

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=CategoryOut)
async def create(data: CategoryCreate):
	category = await create_category(data)
	return CategoryOut(
		id=str(category.id),
		name=category.name,
		slug=category.slug,
		description=category.description,
		image=category.image,
		is_active=category.is_active
	)

@router.get("/", response_model=list[CategoryOut])
async def get_all():
    categories = await list_categories()
    return [
        CategoryOut(
            id=str(cat.id),
            name=cat.name,
            slug=cat.slug,
            description=cat.description,
            image=cat.image,
            is_active=cat.is_active
        )
        for cat in categories
    ]

# update category
@router.put("/{category_id}")
async def update(category_id: str, data: CategoryCreate):
    ok = await update_category(category_id, data.dict(exclude_none=True))

    if not ok:
        raise HTTPException(status_code=404, detail="Category not found")

    return {"message": "Category updated successfully"}

# delete category
@router.delete("/{category_id}")
async def delete(category_id: str):
    ok = await delete_category(category_id)

    if not ok:
        raise HTTPException(status_code=404, detail="Category not found")

    return {"message": "Category deleted successfully"}