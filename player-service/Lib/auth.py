from jose import JWTError, jwt
from fastapi import HTTPException, Depends, Request
from datetime import datetime, timedelta
from redis_client import r

SECRET_KEY = "e4VaWz9Fj2_dQaYpUe6L9k9qAaXq2QJZT_6QijD5D7JmTkHcWybSHl0rYiByZKFcOmSDT3r-qHTIowHjWmMl6w"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    r.set(token, "valid", ex=ACCESS_TOKEN_EXPIRE_MINUTES*60)
    return token

def verify_token(token: str):
    if not r.get(token):
        raise HTTPException(status_code=401, detail="Token expired or revoked")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")

def get_current_user(request: Request):
    token = request.headers.get("Authorization")
    if token is None or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = token.split(" ")[1]
    return verify_token(token)
