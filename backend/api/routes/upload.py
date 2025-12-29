"""File upload endpoints."""
import logging
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from backend.config import settings
from backend.models.schemas import FileUploadResponse
from backend.services.document_service import DocumentService

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/upload-pdf", response_model=FileUploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    document_service = DocumentService()
    
    if not document_service.validate_file(file.filename):
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    try:
        file_path = settings.upload_path / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        chunks_added = await document_service.process_pdf(file_path)
        return FileUploadResponse(
            status="success", filename=file.filename, chunks_added=chunks_added
        )
    except Exception as e:
        return FileUploadResponse(status="error", message=str(e))