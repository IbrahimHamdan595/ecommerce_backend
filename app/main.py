from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection

from app.routers import auth_router
from app.routers import address_router
from app.routers import category_router, product_router, cart_router

@asynccontextmanager
async def lifespan(app: FastAPI):
	# start up
	await connect_to_mongo()
	print("MongoDB connected")
	yield
	# shutdown
	print("Closing MongoDB ..")
	await close_mongo_connection()

app = FastAPI(
	title=settings.PROJECT_NAME,
	openapi_url=f"{settings.API_V1_STR}/openapi.json",
	lifespan=lifespan
)

app.include_router(auth_router.router, prefix=settings.API_V1_STR)
app.include_router(address_router.router, prefix=settings.API_V1_STR)
app.include_router(category_router.router, prefix=settings.API_V1_STR)
app.include_router(product_router.router, prefix=settings.API_V1_STR)
app.include_router(cart_router.router, prefix=settings.API_V1_STR)

# CORS
app.add_middleware(
	CORSMiddleware,
	allow_origins = settings.BACKEND_CORS_ORIGINS,
	allow_credentials = True,
	allow_methods = ["*"],
	allow_headers = ["*"]
)

# simple health check
@app.get("/heatlh", tags=["health"])
async def health_check():
	return {"status": "ok", "message": "E-Commerce API is running"}
