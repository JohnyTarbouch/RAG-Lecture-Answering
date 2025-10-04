from fastapi import APIRouter, FastAPI
import os

base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)

@base_router.get('/')
async def welcome_message():
    app_name = os.getenv("APP_NAME", "RAG")
    return {
        "message": f"Welcome to the {app_name} API"
    }