from fastapi import APIRouter

from app.routes.endpoints import resource_router

router = APIRouter()

router.include_router(resource_router.router)