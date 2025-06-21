import uuid
import time
from typing import List, Dict, Any, Optional
from datetime import datetime
from app.services.document_processor import document_processor
from app.services.vector_store import vector_store
from app.services.gemini_service import gemini_service
from app.models.document import DocumentResponse, DocumentSummary
from app.models.chat import ChatResponse, ChatSource

class RAGService:
    def __init__(self):
        self.documents_store = {}  # In-memory store for document metadata
        self.chat_history = {}     # In-memory store for chat history
    
    async def process_document(self, file_content: bytes, filename: str, 
                             content_type: str) -> DocumentResponse:
        """Process uploaded document and store in vector database."""
        try:
            # Generate document ID
            document_id = str(uuid.uuid4())
            
            # Save file
            file_path = await document_processor.save_uploaded_file(file_content, filename)
            
            # Extract text
            text, metadata = document_processor.extract_text_from_file(file_path, filename)
            if not text:
                raise Exception("Failed to extract text from document")
            
            # Create text chunks
            chunks = document_processor.chunk_text(text, filename)
            if not chunks:
                raise Exception("Failed to create text chunks")
            
            # Store chunks in vector database
            success = vector_store.add_document_chunks(document_id, chunks, filename)
            if not success:
                raise Exception("Failed to store document in vector database")
            
            # Create document response
            doc_response = DocumentResponse(
                id=document_id,
                filename=filename,
                content_type=content_type,
                size=len(file_content),
                upload_date=datetime.now(),
                page_count=metadata.get("page_count"),
                word_count=metadata.get("word_count", len(text.split())),
                status="processed"
            )
            
            # Store document metadata
            self.documents_store[document_id] = {
                "document": doc_response,
                "file_path": file_path,
                "text": text,
                "metadata": metadata,
                "chunks_count": len(chunks)
            }
            
            return doc_response
            
        except Exception as e:
            print(f"Error processing document: {e}")
            raise Exception(f"Document processing failed: {str(e)}")
    
    async def generate_document_summary(self, document_id: str) -> DocumentSummary:
        """Generate AI-powered summary for a document."""
        try:
            if document_id not in self.documents_store:
                raise Exception("Document not found")
            
            doc_data = self.documents_store[document_id]
            text = doc_data["text"]
            
            # Generate summary using Gemini
            summary_data = await gemini_service.generate_summary(text)
            
            # Create summary response
            summary = DocumentSummary(
                document_id=document_id,
                summary=summary_data["summary"],
                key_points=summary_data["key_points"],
                word_count=len(text.split()),
                generated_at=datetime.now()
            )
            
            return summary
            
        except Exception as e:
            print(f"Error generating summary: {e}")
            raise Exception(f"Summary generation failed: {str(e)}")
    
    async def ask_question(self, question: str, document_ids: Optional[List[str]] = None,
                          max_sources: int = 5) -> ChatResponse:
        """Answer question using RAG approach."""
        try:
            start_time = time.time()
            
            # Search for relevant chunks
            relevant_chunks = vector_store.search_similar_chunks(
                query=question,
                document_ids=document_ids,
                top_k=max_sources
            )
            
            if not relevant_chunks:
                return ChatResponse(
                    question=question,
                    answer="I couldn't find relevant information in the uploaded documents to answer your question.",
                    sources=[],
                    response_time=time.time() - start_time,
                    timestamp=datetime.now(),
                    document_ids=document_ids or []
                )
            
            # Prepare context from relevant chunks
            context_parts = []
            sources = []
            
            for chunk in relevant_chunks:
                context_parts.append(f"From {chunk['filename']}:\n{chunk['content']}")
                
                # Create source information
                source = ChatSource(
                    document_id=chunk["document_id"],
                    document_name=chunk["filename"],
                    page_number=chunk["metadata"].get("page_number"),
                    chunk_text=chunk["content"][:200] + "..." if len(chunk["content"]) > 200 else chunk["content"],
                    relevance_score=chunk["similarity_score"]
                )
                sources.append(source)
            
            context = "\n\n---\n\n".join(context_parts)
            
            # Generate answer using Gemini
            answer = await gemini_service.generate_response(question, context)
            
            # Create chat response
            chat_response = ChatResponse(
                question=question,
                answer=answer,
                sources=sources,
                response_time=time.time() - start_time,
                timestamp=datetime.now(),
                document_ids=document_ids or []
            )
            
            # Store in chat history
            if document_ids:
                for doc_id in document_ids:
                    if doc_id not in self.chat_history:
                        self.chat_history[doc_id] = []
                    self.chat_history[doc_id].append(chat_response)
            
            return chat_response
            
        except Exception as e:
            print(f"Error answering question: {e}")
            return ChatResponse(
                question=question,
                answer=f"I encountered an error while processing your question: {str(e)}",
                sources=[],
                response_time=time.time() - start_time,
                timestamp=datetime.now(),
                document_ids=document_ids or []
            )
    
    async def compare_documents(self, document_ids: List[str]) -> Dict[str, Any]:
        """Compare multiple documents and find similarities/differences."""
        try:
            if len(document_ids) < 2:
                raise Exception("At least 2 documents are required for comparison")
            
            # Get document contents
            doc_contents = []
            doc_names = []
            
            for doc_id in document_ids:
                if doc_id not in self.documents_store:
                    raise Exception(f"Document {doc_id} not found")
                
                doc_data = self.documents_store[doc_id]
                doc_contents.append(doc_data["text"])
                doc_names.append(doc_data["document"].filename)
            
            # Use Gemini to compare documents
            comparison_result = await gemini_service.compare_documents(doc_contents, doc_names)
            
            # Add document metadata
            comparison_result["documents"] = [
                {
                    "id": doc_id,
                    "filename": self.documents_store[doc_id]["document"].filename,
                    "word_count": self.documents_store[doc_id]["document"].word_count
                }
                for doc_id in document_ids
            ]
            
            return comparison_result
            
        except Exception as e:
            print(f"Error comparing documents: {e}")
            raise Exception(f"Document comparison failed: {str(e)}")
    
    def get_document(self, document_id: str) -> Optional[DocumentResponse]:
        """Get document by ID."""
        if document_id in self.documents_store:
            return self.documents_store[document_id]["document"]
        return None
    
    def get_all_documents(self) -> List[DocumentResponse]:
        """Get all processed documents."""
        return [data["document"] for data in self.documents_store.values()]
    
    def delete_document(self, document_id: str) -> bool:
        """Delete document and its chunks from vector store."""
        try:
            if document_id not in self.documents_store:
                return False
            
            doc_data = self.documents_store[document_id]
            
            # Delete from vector store
            vector_store.delete_document_chunks(document_id)
            
            # Delete file
            document_processor.delete_file(doc_data["file_path"])
            
            # Remove from store
            del self.documents_store[document_id]
            
            # Clean up chat history
            if document_id in self.chat_history:
                del self.chat_history[document_id]
            
            return True
            
        except Exception as e:
            print(f"Error deleting document: {e}")
            return False
    
    def get_chat_history(self, document_id: str) -> List[ChatResponse]:
        """Get chat history for a document."""
        return self.chat_history.get(document_id, [])
    
    def clear_chat_history(self, document_id: str) -> bool:
        """Clear chat history for a document."""
        try:
            if document_id in self.chat_history:
                del self.chat_history[document_id]
            return True
        except Exception as e:
            print(f"Error clearing chat history: {e}")
            return False
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics."""
        try:
            vector_stats = vector_store.get_collection_stats()
            
            return {
                "total_documents": len(self.documents_store),
                "total_chunks": vector_stats.get("total_chunks", 0),
                "total_conversations": sum(len(history) for history in self.chat_history.values()),
                "vector_store_stats": vector_stats,
                "embedding_model": vector_stats.get("embedding_model", "unknown")
            }
        except Exception as e:
            print(f"Error getting system stats: {e}")
            return {"error": str(e)}
    
    async def find_similar_documents(self, document_id: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Find documents similar to a given document."""
        try:
            if document_id not in self.documents_store:
                raise Exception("Document not found")
            
            similar_docs = vector_store.find_similar_documents(document_id, top_k)
            
            # Enrich with document metadata
            enriched_docs = []
            for sim_doc in similar_docs:
                if sim_doc["document_id"] in self.documents_store:
                    doc_data = self.documents_store[sim_doc["document_id"]]
                    enriched_doc = {
                        **sim_doc,
                        "document_info": doc_data["document"],
                        "metadata": doc_data["metadata"]
                    }
                    enriched_docs.append(enriched_doc)
            
            return enriched_docs
            
        except Exception as e:
            print(f"Error finding similar documents: {e}")
            return []

# Global instance
rag_service = RAGService() 