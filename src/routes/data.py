from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from src.helper.config import get_settings, Settings
from fastapi.responses import JSONResponse
from src.controller import DataController
from src.controller import ProjectController
import aiofiles 
import os


data_router = APIRouter(
    prefix = "/api/v1",
    tags = [ "api_v1" ],
)

@data_router.post("/upload/{project_id}")
async def upload_file(project_id: str, file : UploadFile):
    
    is_valid, result_status = DataController().validate_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {
                    "Status": result_status.value
                }
        )

    project_path = ProjectController().get_project_dir_path(project_id=project_id)

    file_path = os.path.join(
        project_path,
        file.filename
    )


    async with aiofiles.open(file_path, "wb") as f:
        while chunk := await file.read(get_settings().FILE_DEFAULT_CHUNK_SIZE):
            await f.write(chunk)

    return JSONResponse(
            content = {
                    "Status": result_status.value
            }
    )