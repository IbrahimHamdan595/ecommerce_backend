from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from app.schemas.user_schema import RegisterSchema, LoginSchema, UserOut
from app.services.user_service import create_user, authenticate_user, get_user_by_email
from app.utils.jwt import create_access_token
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = HTTPBearer()

# Register
@router.post("/register")
async def register(data: RegisterSchema):
	existing = await get_user_by_email(data.email)
	if existing:
		raise HTTPException(status_code=400, detail = "Email already exists")

	user = await create_user(data)
	return {"message": "User registered successfully"}

# Login
@router.post("/login")
async def login(data: LoginSchema):
	user = await authenticate_user(data.email, data.password)
	if not user:
		raise HTTPException(status_code=400, detail = "Invaild email or password")

	token = create_access_token({"sub": user.email})
	return {"access_token": token, "token_type": "bearer"}

# Current User
async def get_current_user(creds: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    token = creds.credentials
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        email = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.get("/me", response_model=UserOut)
async def get_me(user=Depends(get_current_user)):
    return UserOut(
        id=str(user.id),
        full_name=user.full_name,
        email=user.email,
        phone=user.phone,
        role=user.role,
        is_verified=user.is_verified,
    )