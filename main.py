from fastapi import FastAPI
from routs.base import base_router
from routs.data import data_router

app = FastAPI()

app.include_router(base_router)
app.include_router(data_router)
