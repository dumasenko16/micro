import time
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import mongoengine
from prometheus_fastapi_instrumentator import Instrumentator

import router
import auth.router as auth_router
from deps import init_tracer
from config import DB_NAME

logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    logger.info("Connected to base")
    mongoengine.connect(host=f"mongodb://mongo_product:27017/{DB_NAME}", alias=DB_NAME)
    init_tracer()
    Instrumentator().instrument(app).expose(app)


@app.on_event("shutdown")
async def shutdown():
    logger.info("Disconnected to base")
    mongoengine.disconnect(alias=DB_NAME)


@app.get('/_health')
async def health_check():
    return {
        'status': 'Ok'
    }

app.include_router(router.user_router, prefix='/v1')
app.include_router(auth_router.router, prefix='/v1')
