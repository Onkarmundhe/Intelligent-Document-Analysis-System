import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional, Tuple
import uuid
import json
from datetime import datetime
from app.core.config import settings

class VectorStore:
    def __init__(self):
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=settings.chroma_persist_dir,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer(settings.embedding_model)
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_document_chunks(self, document_id: str, chunks: List[Dict[str, Any]], 
                          filename: str) -> bool:
        """Add document chunks to vector store."""
        try:
            # Prepare data for ChromaDB
            ids = []
            documents = []
            metadatas = []
            
            for i, chunk in enumerate(chunks):
                chunk_id = f"{document_id}_{i}"
                ids.append(chunk_id)
                documents.append(chunk["content"])
                
                # Prepare metadata
                metadata = {
                    "document_id": document_id,
                    "filename": filename,
                    "chunk_index": chunk["chunk_index"],
                    "start_char": chunk["start_char"],
                    "end_char": chunk["end_char"],
                    "created_at": datetime.now().isoformat(),
                    **chunk.get("metadata", {})
                }
                metadatas.append(metadata)
            
            # Generate embeddings
            embeddings = self.embedding_model.encode(documents).tolist()
            
            # Add to ChromaDB
            self.collection.add(
                ids=ids,
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas
            )
            
            return True
            
        except Exception as e:
            print(f"Error adding document chunks: {e}")
            return False
    
    def search_similar_chunks(self, query: str, document_ids: Optional[List[str]] = None, 
                            top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar chunks using semantic similarity."""
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode([query]).tolist()
            
            # Prepare where clause for filtering by document IDs
            where_clause = None
            if document_ids:
                where_clause = {"document_id": {"$in": document_ids}}
            
            # Search in ChromaDB
            results = self.collection.query(
                query_embeddings=query_embedding,
                n_results=top_k,
                where=where_clause,
                include=["documents", "metadatas", "distances"]
            )
            
            # Format results
            chunks = []
            if results["documents"] and len(results["documents"]) > 0:
                for i in range(len(results["documents"][0])):
                    chunk = {
                        "content": results["documents"][0][i],
                        "metadata": results["metadatas"][0][i],
                        "similarity_score": 1 - results["distances"][0][i],  # Convert distance to similarity
                        "document_id": results["metadatas"][0][i]["document_id"],
                        "filename": results["metadatas"][0][i]["filename"],
                        "chunk_index": results["metadatas"][0][i]["chunk_index"]
                    }
                    chunks.append(chunk)
            
            return chunks
            
        except Exception as e:
            print(f"Error searching similar chunks: {e}")
            return []
    
    def get_document_chunks(self, document_id: str) -> List[Dict[str, Any]]:
        """Get all chunks for a specific document."""
        try:
            results = self.collection.get(
                where={"document_id": document_id},
                include=["documents", "metadatas"]
            )
            
            chunks = []
            if results["documents"]:
                for i in range(len(results["documents"])):
                    chunk = {
                        "content": results["documents"][i],
                        "metadata": results["metadatas"][i],
                        "document_id": results["metadatas"][i]["document_id"],
                        "filename": results["metadatas"][i]["filename"],
                        "chunk_index": results["metadatas"][i]["chunk_index"]
                    }
                    chunks.append(chunk)
            
            # Sort by chunk index
            chunks.sort(key=lambda x: x["chunk_index"])
            return chunks
            
        except Exception as e:
            print(f"Error getting document chunks: {e}")
            return []
    
    def delete_document_chunks(self, document_id: str) -> bool:
        """Delete all chunks for a specific document."""
        try:
            # Get all chunk IDs for the document
            results = self.collection.get(
                where={"document_id": document_id},
                include=["documents"]
            )
            
            if results["ids"]:
                self.collection.delete(ids=results["ids"])
            
            return True
            
        except Exception as e:
            print(f"Error deleting document chunks: {e}")
            return False
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store."""
        try:
            count = self.collection.count()
            
            # Get unique documents
            results = self.collection.get(include=["metadatas"])
            unique_docs = set()
            if results["metadatas"]:
                for metadata in results["metadatas"]:
                    unique_docs.add(metadata["document_id"])
            
            return {
                "total_chunks": count,
                "unique_documents": len(unique_docs),
                "embedding_model": settings.embedding_model,
                "collection_name": self.collection.name
            }
            
        except Exception as e:
            print(f"Error getting collection stats: {e}")
            return {"error": str(e)}
    
    def find_similar_documents(self, document_id: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Find documents similar to a given document."""
        try:
            # Get chunks from the source document
            source_chunks = self.get_document_chunks(document_id)
            if not source_chunks:
                return []
            
            # Use the first few chunks as representative text
            representative_text = " ".join([chunk["content"] for chunk in source_chunks[:3]])
            
            # Search for similar chunks in other documents
            similar_chunks = self.search_similar_chunks(
                query=representative_text,
                top_k=top_k * 3  # Get more to filter out the source document
            )
            
            # Group by document and calculate average similarity
            doc_similarities = {}
            for chunk in similar_chunks:
                chunk_doc_id = chunk["document_id"]
                if chunk_doc_id != document_id:  # Exclude source document
                    if chunk_doc_id not in doc_similarities:
                        doc_similarities[chunk_doc_id] = {
                            "document_id": chunk_doc_id,
                            "filename": chunk["filename"],
                            "similarities": [],
                            "chunks": []
                        }
                    doc_similarities[chunk_doc_id]["similarities"].append(chunk["similarity_score"])
                    doc_similarities[chunk_doc_id]["chunks"].append(chunk)
            
            # Calculate average similarity for each document
            similar_docs = []
            for doc_data in doc_similarities.values():
                avg_similarity = sum(doc_data["similarities"]) / len(doc_data["similarities"])
                similar_docs.append({
                    "document_id": doc_data["document_id"],
                    "filename": doc_data["filename"],
                    "average_similarity": avg_similarity,
                    "matching_chunks": len(doc_data["chunks"]),
                    "sample_chunks": doc_data["chunks"][:2]  # Include a few sample chunks
                })
            
            # Sort by similarity and return top results
            similar_docs.sort(key=lambda x: x["average_similarity"], reverse=True)
            return similar_docs[:top_k]
            
        except Exception as e:
            print(f"Error finding similar documents: {e}")
            return []
    
    def update_chunk_metadata(self, document_id: str, metadata_updates: Dict[str, Any]) -> bool:
        """Update metadata for all chunks of a document."""
        try:
            # Get all chunks for the document
            results = self.collection.get(
                where={"document_id": document_id},
                include=["metadatas"]
            )
            
            if not results["ids"]:
                return False
            
            # Update metadata
            updated_metadatas = []
            for metadata in results["metadatas"]:
                updated_metadata = {**metadata, **metadata_updates}
                updated_metadatas.append(updated_metadata)
            
            # Update in ChromaDB
            self.collection.update(
                ids=results["ids"],
                metadatas=updated_metadatas
            )
            
            return True
            
        except Exception as e:
            print(f"Error updating chunk metadata: {e}")
            return False

# Global instance
vector_store = VectorStore() 