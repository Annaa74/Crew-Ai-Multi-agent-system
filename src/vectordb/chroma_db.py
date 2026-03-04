"""
Vector Database Integration using Chromadb
Stores and retrieves resume/JD embeddings for semantic search and matching
"""

import os
from typing import List, Dict, Optional, Any
import chromadb
from chromadb.config import Settings
import json
from datetime import datetime


class ChromaVectorDB:
    """Wrapper for Chroma vector database operations"""
    
    def __init__(self, persist_dir: Optional[str] = None, collection_name: str = "hiring_assistants"):
        """
        Initialize Chroma vector database
        
        Args:
            persist_dir: Directory to persist vectors (for local mode)
            collection_name: Name of the collection to use
        """
        self.persist_dir = persist_dir or os.getenv("CHROMA_PERSIST_DIRECTORY", "./data/chroma")
        self.collection_name = collection_name
        
        # Create persist directory if it doesn't exist
        os.makedirs(self.persist_dir, exist_ok=True)
        
        # Initialize Chroma client with persistence
        self.client = chromadb.PersistentClient(path=self.persist_dir)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_job_description(self, job_id: str, job_title: str, job_text: str, 
                           metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Add a job description to the vector database
        
        Args:
            job_id: Unique identifier for the job
            job_title: Title of the job
            job_text: Full job description text
            metadata: Additional metadata to store
            
        Returns:
            Job ID
        """
        doc_metadata = metadata or {}
        doc_metadata.update({
            "type": "job_description",
            "job_title": job_title,
            "created_at": datetime.now().isoformat()
        })
        
        self.collection.add(
            ids=[f"job_{job_id}"],
            documents=[job_text],
            metadatas=[doc_metadata]
        )
        
        return job_id
    
    def add_resume(self, resume_id: str, candidate_name: str, resume_text: str,
                  metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Add a resume to the vector database
        
        Args:
            resume_id: Unique identifier for the resume
            candidate_name: Name of the candidate
            resume_text: Full resume text
            metadata: Additional metadata to store
            
        Returns:
            Resume ID
        """
        doc_metadata = metadata or {}
        doc_metadata.update({
            "type": "resume",
            "candidate_name": candidate_name,
            "created_at": datetime.now().isoformat()
        })
        
        self.collection.add(
            ids=[f"resume_{resume_id}"],
            documents=[resume_text],
            metadatas=[doc_metadata]
        )
        
        return resume_id
    
    def find_matching_resumes(self, job_description: str, top_k: int = 5) -> List[Dict]:
        """
        Find resumes that match a job description
        
        Args:
            job_description: Job description to search for
            top_k: Number of top matches to return
            
        Returns:
            List of matching resumes with similarity scores
        """
        results = self.collection.query(
            query_texts=[job_description],
            n_results=top_k,
            where={"type": "resume"}
        )
        
        matches = []
        for i in range(len(results["ids"][0])):
            matches.append({
                "id": results["ids"][0][i],
                "score": float(results["distances"][0][i]),
                "metadata": results["metadatas"][0][i],
                "document": results["documents"][0][i][:500] + "..."  # Preview
            })
        
        return matches
    
    def find_matching_jobs(self, resume_text: str, top_k: int = 5) -> List[Dict]:
        """
        Find job descriptions that match a resume
        
        Args:
            resume_text: Resume text to search for
            top_k: Number of top matches to return
            
        Returns:
            List of matching jobs with similarity scores
        """
        results = self.collection.query(
            query_texts=[resume_text],
            n_results=top_k,
            where={"type": "job_description"}
        )
        
        matches = []
        for i in range(len(results["ids"][0])):
            matches.append({
                "id": results["ids"][0][i],
                "score": float(results["distances"][0][i]),
                "metadata": results["metadatas"][0][i],
                "document": results["documents"][0][i][:500] + "..."  # Preview
            })
        
        return matches
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection"""
        count = self.collection.count()
        
        # Get sample of documents to analyze
        all_docs = self.collection.get(limit=count)
        
        job_count = sum(1 for m in all_docs["metadatas"] if m.get("type") == "job_description")
        resume_count = sum(1 for m in all_docs["metadatas"] if m.get("type") == "resume")
        
        return {
            "total_documents": count,
            "job_descriptions": job_count,
            "resumes": resume_count,
            "collection_name": self.collection_name,
            "persist_directory": self.persist_dir
        }
    
    def clear_collection(self):
        """Clear all documents from the collection"""
        # Delete the collection and recreate it
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    
    def export_data(self, output_file: str = "vector_db_export.json"):
        """Export collection data to JSON file"""
        count = self.collection.count()
        all_docs = self.collection.get(limit=count)
        
        export_data = {
            "collection": self.collection_name,
            "exported_at": datetime.now().isoformat(),
            "total_documents": count,
            "documents": []
        }
        
        for i in range(len(all_docs["ids"])):
            export_data["documents"].append({
                "id": all_docs["ids"][i],
                "metadata": all_docs["metadatas"][i],
                "document_preview": all_docs["documents"][i][:200] + "..."
            })
        
        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return output_file


# Singleton instance
_vector_db = None


def get_vector_db(persist_dir: Optional[str] = None) -> ChromaVectorDB:
    """Get or create singleton vector database instance"""
    global _vector_db
    if _vector_db is None:
        _vector_db = ChromaVectorDB(persist_dir=persist_dir)
    return _vector_db
