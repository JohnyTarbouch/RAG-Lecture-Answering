from fastapi import APIRouter, FastAPI, Depends
import os
from helper.config import get_settings, Settings

base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)

@base_router.get('/')
async def welcome_message(app_settings: Settings = Depends(get_settings)):
    app_name = app_settings.APP_NAME
    return {
        "message": f"Welcome to the {app_name} API"
    }