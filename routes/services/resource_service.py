import shutil
from os import listdir, makedirs, path

from fastapi import HTTPException

from utils.config import ROOT_DIR


class ResourceService:
    def _get_resource_path(self, name: str) -> str:
        """Helper to generate the resource path."""
        return path.join(ROOT_DIR, f"{name}s")

    def _check_resource_exists(self, resource_path: str):
        """Helper to check if a resource exists, raising an exception if not."""
        if not path.exists(resource_path):
            raise HTTPException(status_code=404, detail="Resource not found")

    async def create_directory(self, name: str) -> dict:
        resource_path = self._get_resource_path(name)
        makedirs(resource_path, exist_ok=True)
        return {"message": f"Directory '{name}s' created successfully."}

    async def list_available(self) -> list[str]:
        resources = listdir(ROOT_DIR)
        return resources

    async def delete_resource(self, resource_name: str) -> dict:
        resource_path = self._get_resource_path(resource_name)
        self._check_resource_exists(resource_path)
        shutil.rmtree(resource_path)
        return {"message": f"Resource '{resource_name}s' deleted successfully."}
