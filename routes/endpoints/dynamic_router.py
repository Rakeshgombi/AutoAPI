import os

from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse

from routes.services.records_service import RecordService


def create_dynamic_routes(app: FastAPI, root_dir: str):
    """
    Dynamically create routes based on the directory structure.
    """
    records_service = RecordService()

    if not os.path.exists(root_dir):
        raise FileNotFoundError(f"Root directory '{root_dir}' does not exist.")

    for resource in os.listdir(root_dir):
        resource_path = os.path.join(root_dir, resource)
        records_service.resource_path = resource_path
        if os.path.isdir(resource_path):
            router = APIRouter(prefix=f"/{resource.replace('_', '-')}", tags=[resource])

            @router.get("", response_model=list[dict])
            async def list_entries(
                resource_path=resource_path, offset: int = 0, limit: int = 10
            ):
                entries = await records_service.get_records(resource_path)
                return JSONResponse(content=entries[offset : offset + limit])

            @router.get("/{entry_id}", response_model=dict)
            async def get_entry(entry_id: str, resource_path=resource_path):
                entry = await records_service.get_record(resource_path, entry_id)
                return JSONResponse(content=entry)

            @router.post("", response_model=dict)
            async def create_entry(data: dict, resource_path=resource_path):
                response = await records_service.create_record(resource_path, data)
                return JSONResponse(content=response)

            @router.put("/{entry_id}", response_model=dict)
            async def update_entry(
                entry_id: str, data: dict, resource_path=resource_path
            ):
                response = await records_service.update_record(
                    resource_path, entry_id, data
                )
                return JSONResponse(content=response)

            @router.delete("/{entry_id}", response_model=dict)
            async def delete_entry(entry_id: str, resource_path=resource_path):
                response = await records_service.delete_record(resource_path, entry_id)
                return JSONResponse(content=response)

            app.include_router(router)
