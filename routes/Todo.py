from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from datetime import datetime
from typing import List
from supabase import create_client, Client
from supabase.py import Database
from auth import validate_token
from schemas.Todo import Todo, TodoCreate, TodoUpdate

supabase_url: str = os.getenv("SUPABASE_URL")
supabase_key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

todo_router = APIRouter()

class TodoService:
    def get_all_todos(self, user_id: str) -> List[Todo]:
        data = supabase.from_("todos").select("*").eq("user_id", user_id)
        return data.execute()

    def get_todo(self, todo_id: str, user_id: str) -> Todo:
        data = supabase.from_("todos").select("*").eq("id", todo_id).eq("user_id", user_id)
        result = data.execute()
        if not result.data:
            raise HTTPException(status_code=404, detail="Todo not found")
        return Todo(**result.data[0])

    def create_todo(self, todo: TodoCreate, user_id: str) -> Todo:
        data = supabase.from_("todos").insert([todo.dict()]).eq("user_id", user_id)
        return Todo(**data.execute()[0])

    def update_todo(self, todo_id: str, todo: TodoUpdate, user_id: str) -> Todo:
        data = supabase.from_("todos").update(todo.dict()).eq("id", todo_id).eq("user_id", user_id)
        return Todo(**data.execute()[0])

    def delete_todo(self, todo_id: str, user_id: str):
        supabase.from_("todos").delete().eq("id", todo_id).eq("user_id", user_id)

todo_service = TodoService()

@todo_router.get("/todos", response_model=List[Todo])
async def get_all_todos(token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    user_id = validate_token(token.credentials)
    return todo_service.get_all_todos(user_id)

@todo_router.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: str, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    user_id = validate_token(token.credentials)
    return todo_service.get_todo(todo_id, user_id)

@todo_router.post("/todos", response_model=Todo)
async def create_todo(todo: TodoCreate, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    user_id = validate_token(token.credentials)
    return todo_service.create_todo(todo, user_id)

@todo_router.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: str, todo: TodoUpdate, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    user_id = validate_token(token.credentials)
    return todo_service.update_todo(todo_id, todo, user_id)

@todo_router.delete("/todos/{todo_id}")
async def delete_todo(todo_id: str, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    user_id = validate_token(token.credentials)
    todo_service.delete_todo(todo_id, user_id)
    return {"message": "Todo deleted successfully"}