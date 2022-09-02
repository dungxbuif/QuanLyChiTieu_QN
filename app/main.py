import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers.api import api_router
from app.core.config import settings
from app.initial_data import init_data

logging.getLogger().handlers.clear()
app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json",
)
# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins = settings.BACKEND_CORS_ORIGINS,
        allow_credentials =True,
        allow_methods = ["*"],
        allow_headers = ["*"],
    )
app.include_router(api_router, prefix=settings.API_V1_STR)
init_data()
@app.get("/")
def root():
    return {"message": "Hello World!"}
