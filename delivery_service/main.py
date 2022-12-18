from fastapi import FastAPI, Request
from router import delivery_router

app = FastAPI()

app.include_router(delivery_router, prefix='/v1')

