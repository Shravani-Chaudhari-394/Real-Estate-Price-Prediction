"""Authentication service."""

import os
from datetime import datetime, timedelta
from functools import lru_cache

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = os.getenv("SECRET_KEY", "capstone-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer(auto_error=False)


@lru_cache
def _get_users_db() -> dict:
    return {
        "admin": {
            "username": "admin",
            "hashed_password": pwd_context.hash("admin123"),
            "role": "admin",
        },
        "analyst": {
            "username": "analyst",
            "hashed_password": pwd_context.hash("analyst123"),
            "role": "analyst",
        },
    }


def authenticate_user(username: str, password: str) -> dict | None:
    user = _get_users_db().get(username)
    if not user or not pwd_context.verify(password, user["hashed_password"]):
        return None
    return {"username": user["username"], "role": user["role"]}


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    if credentials is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"username": username, "role": _get_users_db().get(username, {}).get("role", "user")}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
