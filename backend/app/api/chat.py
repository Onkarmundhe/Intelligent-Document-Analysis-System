from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.models.chat import ChatRequest, ChatResponse
from app.services.rag_service import rag_service

router = APIRouter()

@router.post("/chat/ask", response_model=ChatResponse)
async def ask_question(request: ChatRequest):
    """Ask a question about uploaded documents."""
    try:
        response = await rag_service.ask_question(
            question=request.question,
            document_ids=request.document_ids,
            max_sources=request.max_sources
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat/history/{document_id}", response_model=List[ChatResponse])
async def get_chat_history(document_id: str):
    """Get chat history for a specific document."""
    try:
        history = rag_service.get_chat_history(document_id)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/chat/history/{document_id}")
async def clear_chat_history(document_id: str):
    """Clear chat history for a specific document."""
    try:
        success = rag_service.clear_chat_history(document_id)
        if not success:
            raise HTTPException(status_code=404, detail="Document not found")
        return {"message": "Chat history cleared successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat/ask-multiple")
async def ask_multiple_documents(
    question: str,
    document_ids: Optional[List[str]] = None,
    max_sources: int = 5
):
    """Ask a question across multiple documents."""
    try:
        response = await rag_service.ask_question(
            question=question,
            document_ids=document_ids,
            max_sources=max_sources
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 