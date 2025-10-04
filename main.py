from fastapi import FastAPI
from routs.base import base_router
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

app.include_router(base_router)
