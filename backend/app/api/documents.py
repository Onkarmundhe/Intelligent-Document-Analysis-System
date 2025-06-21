from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List, Dict, Any
from app.models.document import DocumentResponse, DocumentSummary
from app.services.rag_service import rag_service
from app.core.config import settings

router = APIRouter()

async def validate_file(file: UploadFile = File(...)):
    """Validate uploaded file."""
    # Check file size
    if file.size > settings.max_file_size:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {settings.max_file_size} bytes"
        )
    
    # Check file extension
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")
    
    file_extension = file.filename.split('.')[-1].lower()
    if file_extension not in settings.allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type not supported. Allowed types: {', '.join(settings.allowed_extensions)}"
        )
    
    return file

@router.post("/documents/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = Depends(validate_file)):
    """Upload and process a document."""
    try:
        # Read file content
        file_content = await file.read()
        
        # Process document
        document = await rag_service.process_document(
            file_content=file_content,
            filename=file.filename,
            content_type=file.content_type
        )
        
        return document
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents/", response_model=List[DocumentResponse])
async def list_documents():
    """Get list of all uploaded documents."""
    try:
        documents = rag_service.get_all_documents()
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: str):
    """Get a specific document by ID."""
    try:
        document = rag_service.get_document(document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        return document
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    """Delete a document and all its data."""
    try:
        success = rag_service.delete_document(document_id)
        if not success:
            raise HTTPException(status_code=404, detail="Document not found")
        return {"message": "Document deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/documents/{document_id}/summarize", response_model=DocumentSummary)
async def summarize_document(document_id: str):
    """Generate AI-powered summary for a document."""
    try:
        summary = await rag_service.generate_document_summary(document_id)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents/{document_id}/similar")
async def find_similar_documents(document_id: str, top_k: int = 3):
    """Find documents similar to the given document."""
    try:
        similar_docs = await rag_service.find_similar_documents(document_id, top_k)
        return {"similar_documents": similar_docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/documents/compare")
async def compare_documents(document_ids: List[str]):
    """Compare multiple documents."""
    try:
        if len(document_ids) < 2:
            raise HTTPException(
                status_code=400, 
                detail="At least 2 document IDs are required"
            )
        
        comparison = await rag_service.compare_documents(document_ids)
        return comparison
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents/stats/system")
async def get_system_stats():
    """Get system statistics."""
    try:
        stats = rag_service.get_system_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 