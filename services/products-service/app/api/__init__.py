from fastapi import APIRouter

from app.api import v1

api_router = APIRouter()
api_router.include_router(v1.api_router, prefix="/v1")