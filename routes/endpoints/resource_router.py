from fastapi import APIRouter
from fastapi.responses import JSONResponse

from routes.services.resource_service import ResourceService

router = APIRouter(tags=["resource"])

resource_service = ResourceService()


@router.get("/create-directory/{name}", response_model=dict)
async def create_directory(name: str):
    response: str = await resource_service.create_directory(name)
    return JSONResponse(content=response)


@router.get("/list-resources", response_model=list)
async def list_available():
    resources: list[str] = await resource_service.list_available()
    return JSONResponse(content=resources)


@router.delete("/delete-resource/{name}")
async def delete_resource(resource_name: str):
    response: dict = await resource_service.delete_resource(resource_name)
    return JSONResponse(content=response)
