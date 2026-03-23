from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from supabase import create_client, Client
from supabase.py import Database
from supabase.exceptions import ClientException
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os
import logging
from logging.config import dictConfig
import uvicorn
from typing import Optional
from routes import User, Todo

# Initialize logging
dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console']
    }
})

# Initialize FastAPI app
app = FastAPI()

# Initialize CORS
origins = [
    os.getenv('CORS_ORIGIN', '*')
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Supabase client
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
SUPABASE_SECRET = os.getenv('SUPABASE_SECRET')

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize JWT secret key
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

# Initialize JWT token expiration time
JWT_TOKEN_EXPIRE_MINUTES = int(os.getenv('JWT_TOKEN_EXPIRE_MINUTES', 30))

# Initialize JWT authentication
security = HTTPBearer()

# Initialize routes
app.include_router(User.router)
app.include_router(Todo.router)

# Health check endpoint
@app.get("/health")
async def health_check():
    return JSONResponse(content={"status": "ok"}, status_code=200)

# Error handler for JWT token validation
@app.exception_handler(JWTError)
async def jwt_error_handler(request: Request, exc: JWTError):
    return JSONResponse(content={"error": "Invalid JWT token"}, status_code=401)

# Error handler for Supabase client exceptions
@app.exception_handler(ClientException)
async def supabase_error_handler(request: Request, exc: ClientException):
    return JSONResponse(content={"error": "Supabase client error"}, status_code=500)

# Error handler for HTTP exceptions
@app.exception_handler(HTTPException)
async def http_error_handler(request: Request, exc: HTTPException):
    return JSONResponse(content={"error": exc.detail}, status_code=exc.status_code)

# Run the app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 8000)))