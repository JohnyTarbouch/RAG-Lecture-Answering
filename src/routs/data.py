from fastapi import APIRouter, FastAPI, Depends, UploadFile, File, status, Request
from fastapi.responses import JSONResponse
import os
from helper.config import get_settings, Settings
from controllers import DataController, ProjectController, ProcessController
import aiofiles
from models import ResponceSignal
import logging
from .schemes.data import ProcessRequest
from models.ProjectModel import ProjectModel
from models.db_schemes import ProjectDBScheme, DataChunkDBScheme
from models.ChunkModel import ChunkModel

logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix="/api/v1/data",
   tags=["api_v1", "data"],
)

@data_router.post('/upload/{project_id}')
async def upload_file(request: Request, project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)):
    project_model = ProjectModel(
        db_client=request.app.db_client
    )
    
    project = await project_model.get_or_create_project(
        project_id=project_id
    )
    
    # Validate file extension
    data_controller_obj = DataController()

    is_valid, signal = data_controller_obj.validate_file(file=file)
    
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'signal': signal,
            }
        )
    
    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    file_path, file_id = data_controller_obj.generate_unique_filepath(
        original_file_name=file.filename,
        project_id=project_id
    ) 
    
    try:
        async with aiofiles.open(file_path, 'wb') as f: # Writing for bin
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):#
                await f.write(chunk)
    except Exception as e:
        logger.error(f'Error while uploading file: {e}')
        
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'signal': ResponceSignal.FILE_UPLOAD_FAILED.value,
            }
        )

    return JSONResponse(
        content={
            'signal': ResponceSignal.FILE_UPLOAD_SUCCESS.value,
            'file_id': file_id,
            # 'project_id': str(project._id),
        }
    )

@data_router.post('/process/{project_id}')
async def process_endpoint(request: Request, project_id: str, process_request: ProcessRequest):
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    process_controller = ProcessController(project_id=project_id)
    do_reset = process_request.do_reset
    
    project_model = ProjectModel(
        db_client=request.app.db_client
    )
    project = await project_model.get_or_create_project(
        project_id=project_id
    )
    
    file_content = process_controller.get_file_content(file_id=file_id)
    file_chunks = process_controller.process_file_content(
        file_content=file_content,
        file_id=file_id,
        chunk_size=chunk_size,
        chunk_overlap=overlap_size
    )
    
    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'signal': ResponceSignal.FILE_PROCESSING_FAILED.value,
            }
        )

    file_chunks_records = [
        DataChunkDBScheme(
            chunk_text=chunk.page_content,
            chunk_metadata=chunk.metadata,
            chunk_order=idx + 1,
            chunk_project_id=project.id
        ) 
        for idx, chunk in enumerate(file_chunks)
    ]
    
    chunk_model = ChunkModel(
        db_client=request.app.db_client
    )
    
    if do_reset:
        deleted_count = await chunk_model.delete_chunk_by_project_id(
            project_id=project.id
        )
        # logger.info(f'Deleted {deleted_count} chunks for project {project_id}')
    
    num_recorded_chunks = await chunk_model.insert_many_chunks(
        chunks=file_chunks_records
    )
    
    return JSONResponse(
        content={
            'signal': ResponceSignal.CHUNK_PROCESSING_SUCCESS.value,
            'inserted_chunks': num_recorded_chunks,
        }
    )

