from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from src.helper.config import get_settings, Settings
from src.model import StatusEnums
from fastapi.responses import JSONResponse
from src.controller import DataController
from src.controller import ProjectController
from src.controller import ProcessController
from src.schemas import ProcessRequest
import aiofiles 

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

    new_filename_with_path, fileKey = DataController().generate_unique_filename_and_return_path(file=file, project_id=project_id)

    saving_file_status = await DataController().save_file(file_path=new_filename_with_path, file=file)

    if saving_file_status == StatusEnums.FILE_UPLOADING_FAILED:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {
                    "Status": saving_file_status.value
            }
         ) 
    return JSONResponse(
            status_code = status.HTTP_201_CREATED,
            content = {
                "Status": StatusEnums.FILE_UPLOADED_SUCCESSFULLY.value
            }
    )


@data_router.post("/process/{project_id}")
async def process_files(project_id: str, process_request: ProcessRequest):
    
    file_id = process_request.file_id 

    file_chunks = ProcessController().chunk_file(project_id=project_id, process_request = process_request)

    if file_chunks is not None:
        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = {
                "Status": StatusEnums.FILE_PROCESSED_SUCCESS.value,
                "Chunks": file_chunks
            }
        )
    else:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {
                    "Status": StatusEnums.FILE_PROCESSED_FAILED.value,
                    "Chunks": file_chunks
            }
         ) 