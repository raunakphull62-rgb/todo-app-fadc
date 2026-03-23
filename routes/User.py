from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from supabase import create_client, Client
from supabase.py import SupabaseError
from jose import jwt
from datetime import datetime, timedelta
from typing import Optional
from config import SUPABASE_URL, SUPABASE_KEY
from auth import verify_token

router = APIRouter()

supabase_url: str = os.getenv("SUPABASE_URL", SUPABASE_URL)
supabase_key: str = os.getenv("SUPABASE_KEY", SUPABASE_KEY)
supabase: Client = create_client(supabase_url, supabase_key)

class User(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str

@router.post("/register", response_model=UserResponse)
async def register_user(user: User):
    try:
        data = supabase.from_("users").insert([{"username": user.username, "password": user.password}]).execute()
        return UserResponse(id=data[0]["id"], username=data[0]["username"])
    except SupabaseError as e:
        raise HTTPException(status_code=400, detail=e.msg)

@router.post("/login")
async def login_user(user: User):
    try:
        data = supabase.from_("users").select("id, username, password").eq("username", user.username).execute()
        if not data:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        if data[0]["password"] != user.password:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        payload = {
            "exp": datetime.utcnow() + timedelta(minutes=30),
            "iat": datetime.utcnow(),
            "sub": data[0]["id"]
        }
        token = jwt.encode(payload, os.getenv("JWT_SECRET"), algorithm="HS256")
        return {"token": token}
    except SupabaseError as e:
        raise HTTPException(status_code=400, detail=e.msg)

@router.get("/me", response_model=UserResponse)
async def get_me(token: HTTPAuthorizationCredentials = Depends(verify_token)):
    try:
        payload = jwt.decode(token.credentials, os.getenv("JWT_SECRET"), algorithms=["HS256"])
        data = supabase.from_("users").select("id, username").eq("id", payload["sub"]).execute()
        return UserResponse(id=data[0]["id"], username=data[0]["username"])
    except SupabaseError as e:
        raise HTTPException(status_code=400, detail=e.msg)