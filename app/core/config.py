from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
	# basic project info
	PROJECT_NAME: str = "E-Commerce Backend"
	API_V1_STR: str = "/api/v1"

	# MongoDB
	MONGODB_URI: str = "mongodb://localhost:27017"
	MONGODB_DB_NAME: str = "ecommerce_db"

	# Security
	JWT_SECRET_KEY: str
	JWT_ALGORITHM: str = "HS256"
	ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

	# Cors
	BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

	model_config = SettingsConfigDict(
		env_file=".env",
		env_file_encoding="utf-8",
		extra="ignore",
	)

settings = Settings()