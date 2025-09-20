# from fastapi import APIRouter, Depends,FastAPI, File, UploadFile ,status 
# from fastapi.responses import JSONResponse
# from models import ResponseSignal
# from helpers.config import get_settings, Settings
# from controllers import DataController ,ProjectController
# import logging

# logger = logging.getLogger('uvicorn.error')

# import aiofiles


# import os

# data_router = APIRouter(
#     prefix="/api/v1/data",
#     tags=['api_v1', 'data']

# )

# @data_router.post("/upload/{project_id}")
# async def upload_data(
#                     project_id: str,
#                     file: UploadFile = File(...),             # <<<<<< مهم
#                     settings: Settings = Depends(get_settings)
#                     ):
#     # Validate file type and size
#     data_controller = DataController()
#     is_valid, result_signal = data_controller.validate_uploaded_file(file=file)

#     # if is_valid:
#     #     return {"message": result_signal}
#     if not is_valid: # is not valid
#         return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
#                              content={"error": result_signal}
#                              ) 


#     project_dir_path = ProjectController().get_project_path(project_id)
#     file_path = data_controller.generate_unique_filename(original_filename=file.filename, project_id=project_id)

#     try:
#         async with aiofiles.open(file_path, 'wb') as out_file:
#             while chunk := await file.read(settings.FILE_DEFAULT_CHUNK_SIZE):  # Read file in chunks
#                 await out_file.write(chunk)  # Write chunk to the destination file
#     except Exception as e:
#         logger.error(f"Error uploading file: {str(e)}")
#         return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                              content={"error": f"Failed to upload file: {str(e)}"}
#                              )
    

#     return JSONResponse(status_code=status.HTTP_201_CREATED,
#                         content=
#                         {
#                             "message": f"File '{file.filename}' uploaded successfully to project '{project_id}'."   }
#                         )   



from fastapi import APIRouter, Depends, File, UploadFile, status, HTTPException
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController
import logging
import os
import aiofiles

logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"],
)

DEFAULT_CHUNK_SIZE = 1024 * 1024  # 1MB

@data_router.post("/upload/{project_id}")
async def upload_data(
    project_id: str,
    file: UploadFile = File(...),
    settings: Settings = Depends(get_settings),
):
    data_controller = DataController()

    # 1) Validate file (may read from stream)
    try:
        is_valid, result_signal = data_controller.validate_uploaded_file(file=file)
    except Exception as e:
        logger.exception("Validation error")
        raise HTTPException(status_code=400, detail="Invalid file") from e

    if not is_valid:
        # return structured client-safe message
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": result_signal},
        )

    # 2) Reset stream position (critical if validator read bytes)
    try:
        # UploadFile has async seek in Starlette 0.40+, otherwise use underlying file
        if hasattr(file, "seek"):
            await file.seek(0)
        else:
            file.file.seek(0)
    except Exception:
        # Fallback to underlying file
        try:
            file.file.seek(0)
        except Exception:
            logger.exception("Failed to reset file stream position")
            raise HTTPException(status_code=500, detail="Failed to process file")

    # 3) Resolve project directory & filename
    project_dir_path = ProjectController().get_project_path(project_id)
    try:
        os.makedirs(project_dir_path, exist_ok=True)
    except Exception:
        logger.exception("Failed to ensure project directory")
        raise HTTPException(status_code=500, detail="Storage is unavailable")

    # Ensure generate_unique_filename returns a safe name (not a path)
    file_path , file_id = data_controller.generate_unique_filepath(
        original_filename=file.filename, project_id=project_id
    )
    # Defensive: drop any path components if function returns something unexpected
    unique_name = os.path.basename(file_id)
    file_path = os.path.join(project_dir_path, unique_name)

    # 4) Write file in chunks
    chunk_size = getattr(settings, "FILE_DEFAULT_CHUNK_SIZE", None) or DEFAULT_CHUNK_SIZE

    try:
        async with aiofiles.open(file_path, "wb") as out_file:
            while True:
                chunk = await file.read(chunk_size)
                if not chunk:
                    break
                await out_file.write(chunk)
    except Exception:
        logger.exception("Error writing uploaded file")
        # Don't leak the actual error to clients
        raise HTTPException(status_code=500, detail="Failed to store file")

    # 5) Success response
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": f"File '{file.filename}' uploaded successfully to project '{project_id}'.",
            "stored_as": unique_name,
            "file_id": file_id,
        },
    )
