from fastapi import APIRouter, HTTPException, Depends

from app.schemas.address_schema import AddressCreate, AddressUpdate, AddressOut
from app.services.address_service import create_address, list_addresses, update_address, delete_address
from app.routers.auth_router import get_current_user

router = APIRouter(prefix="/addresses", tags=["Addresses"])

@router.post("/", response_model=AddressOut)
async def add_address(data: AddressCreate, user=Depends(get_current_user)):
	address = await create_address(str(user.id), data)
	return AddressOut(
		id=str(address.id),
		**data.model_dump()
	)

@router.get("/", response_model=list[AddressOut])
async def get_addresses(user=Depends(get_current_user)):
	addresses = await list_addresses(str(user.id))
	return [
		AddressOut(
			id=str(a.id),
            full_name=a.full_name,
            phone=a.phone,
            country=a.country,
            city=a.city,
            street=a.street,
            building=a.building,
            floor=a.floor,
            additional_info=a.additional_info,
            is_default=a.is_default,
		)
		for a in addresses
	]

@router.put("/{address_id}", response_model=AddressOut)
async def edit_address(address_id: str, data: AddressUpdate, user=Depends(get_current_user)):
	address = await update_address(address_id, str(user.id), data)
	if not address:
		raise HTTPException(status_code=404, detail="Address not found")

	return AddressOut(
		id=str(address.id),
        full_name=address.full_name,
        phone=address.phone,
        country=address.country,
        city=address.city,
        street=address.street,
        building=address.building,
        floor=address.floor,
        additional_info=address.additional_info,
        is_default=address.is_default,
	)

@router.delete("/{address_id}")
async def remove_address(address_id: str, user = Depends(get_current_user)):
	deleted = await delete_address(address_id, str(user.id))
	if not deleted:
		raise HTTPException(status_code=404, detail="Address not found")

	return {"message": "Address deleted successfully"}