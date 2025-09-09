import os
from datetime import timedelta

SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
DATABASE_URL = DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")

