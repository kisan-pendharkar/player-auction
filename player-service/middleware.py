from fastapi import FastAPI, HTTPException, Depends, Form
from jose import jwt
from passlib.context import CryptContext
import redis
from datetime import datetime, timedelta

app = FastAPI()
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

SECRET_KEY = "super-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dummy user DB
fake_users_db = {
    "user1": {
        "username": "user1",
        "hashed_password": pwd_context.hash("password123"),
    }
}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # Store in Redis
    r.setex(token, int((expires_delta or timedelta(minutes=15)).total_seconds()), "valid")
    return token

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    user = fake_users_db.get(username)
    if not user or not verify_password(password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token_data = {"sub": username}
    token = create_access_token(token_data, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": token, "token_type": "bearer"}

