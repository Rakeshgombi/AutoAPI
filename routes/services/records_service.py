import json
from os import listdir, path, remove

from fastapi import HTTPException


class RecordService:
    def _get_file_path(self, resource_path: str, entry_id: str) -> str:
        """Helper to generate file path for a given entry ID."""
        return path.join(resource_path, f"{entry_id}.json")

    def _check_file_exists(self, file_path: str):
        """Helper to check if a file exists, raising an exception if not."""
        if not path.exists(file_path):
            raise HTTPException(status_code=404, detail="Record Not Found")

    def _check_folder_exists(self, folder_path: str):
        """Helper to check if a folder exists, raising an exception if not."""
        folder = path.split(folder_path)[-1]
        if not path.exists(folder_path):
            raise HTTPException(
                status_code=404, detail=f"Resource '{folder}' Not Found"
            )

    async def get_records(self, resource_path: str) -> list[dict]:
        entries = []
        self._check_folder_exists(resource_path)
        for file_name in listdir(resource_path):
            if file_name.endswith(".json"):
                file_path = path.join(resource_path, file_name)
                if path.getsize(file_path) == 0:  # Skip empty files
                    continue
                with open(file_path, "r") as f:
                    try:
                        content = json.load(f)
                    except json.JSONDecodeError:
                        continue  # Skip files with invalid JSON
                entry_id = path.splitext(file_name)[0]
                entries.append({"id": int(entry_id), **content})
        return entries

    async def get_record(self, resource_path: str, entry_id: str) -> dict:
        file_path = self._get_file_path(resource_path, entry_id)
        self._check_folder_exists(resource_path)
        self._check_file_exists(file_path)
        with open(file_path, "r") as f:
            return json.load(f)

    async def create_record(self, resource_path: str, data: dict) -> dict:
        self._check_folder_exists(resource_path)
        file_id = len(listdir(resource_path)) + 1
        file_path = self._get_file_path(resource_path, str(file_id))
        data["id"] = file_id
        with open(file_path, "w") as f:
            json.dump(data, f)
        return {"id": file_id, **data}

    async def update_record(
        self, resource_path: str, entry_id: str, data: dict
    ) -> dict:
        self._check_folder_exists(resource_path)
        file_path = self._get_file_path(resource_path, entry_id)
        self._check_file_exists(file_path)
        with open(file_path, "w") as f:
            f.write(json.dumps(data))
        return {"id": entry_id, **data}

    async def delete_record(self, resource_path: str, entry_id: str) -> dict:
        self._check_folder_exists(resource_path)
        file_path = self._get_file_path(resource_path, entry_id)
        self._check_file_exists(file_path)
        remove(file_path)
        return {"message": "Entry deleted successfully", "id": entry_id}
