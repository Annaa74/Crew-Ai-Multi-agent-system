"""
FastAPI endpoint for the Hiring Assistant with CrewAI agents
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import os
from datetime import datetime
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import custom modules
from src.agents.hiring_agents import HiringAssistantCrew, JDParserAgent, ResumeOptimizerAgent
from src.tools.custom_tools import JDParsingTool, ResomeValidationTool, ResumeOptimizerTool
from src.vectordb.chroma_db import get_vector_db

# Initialize FastAPI app
app = FastAPI(
    title="AI Hiring Assistant API",
    description="CrewAI-powered API for job description parsing and resume optimization",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents and tools
jd_parser_agent = JDParserAgent()
resume_optimizer_agent = ResumeOptimizerAgent()
hiring_crew = HiringAssistantCrew()
vector_db = get_vector_db()

# ==================== Request/Response Models ====================

class JobDescription(BaseModel):
    """Job description input model"""
    job_id: str = Field(..., description="Unique identifier for the job")
    job_title: str = Field(..., description="Title of the job position")
    job_text: str = Field(..., description="Full job description text")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")


class Resume(BaseModel):
    """Resume input model"""
    resume_id: str = Field(..., description="Unique identifier for the resume")
    candidate_name: str = Field(..., description="Name of the candidate")
    resume_text: str = Field(..., description="Full resume text")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")


class JobAnalysisResponse(BaseModel):
    """Response for job description analysis"""
    job_id: str
    job_title: str
    analysis: Dict[str, Any]
    timestamp: str


class ResumeAnalysisResponse(BaseModel):
    """Response for resume analysis/optimization"""
    resume_id: str
    candidate_name: str
    analysis: Dict[str, Any]
    timestamp: str


class HiringRequestResponse(BaseModel):
    """Response for complete hiring request"""
    job_id: str
    resume_id: str
    jd_analysis: Dict[str, Any]
    resume_analysis: Dict[str, Any]
    match_score: float
    timestamp: str


class MatchResult(BaseModel):
    """Single match result"""
    id: str
    score: float
    metadata: Dict[str, Any]
    preview: str


class SearchResponse(BaseModel):
    """Response for search queries"""
    query_type: str
    results: List[MatchResult]
    count: int


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: str


# ==================== Health Check Endpoints ====================

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/stats")
async def get_stats():
    """Get system statistics"""
    vector_db_stats = vector_db.get_collection_stats()
    return {
        "timestamp": datetime.now().isoformat(),
        "vector_database": vector_db_stats
    }


# ==================== Job Description Endpoints ====================

@app.post("/api/v1/jobs/analyze", response_model=JobAnalysisResponse)
async def analyze_job_description(job: JobDescription):
    """
    Analyze a job description and extract key requirements
    
    Returns:
    - Job ID and title
    - Extracted requirements (skills, experience, qualifications)
    - Responsibilities
    - Salary information
    """
    try:
        logger.info(f"Analyzing job description: {job.job_id}")
        
        # Parse the job description
        jd_tool = JDParsingTool()
        analysis = jd_tool._run(job.job_text)
        
        # Store in vector database
        vector_db.add_job_description(
            job.job_id,
            job.job_title,
            job.job_text,
            job.metadata
        )
        
        return {
            "job_id": job.job_id,
            "job_title": job.job_title,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error analyzing job description: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/v1/jobs/upload")
async def upload_job_description(job: JobDescription):
    """Upload a job description to the system"""
    try:
        job_id = vector_db.add_job_description(
            job.job_id,
            job.job_title,
            job.job_text,
            job.metadata
        )
        
        return {
            "success": True,
            "job_id": job_id,
            "message": "Job description uploaded successfully"
        }
    except Exception as e:
        logger.error(f"Error uploading job description: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


# ==================== Resume Endpoints ====================

@app.post("/api/v1/resumes/analyze", response_model=ResumeAnalysisResponse)
async def analyze_resume(resume: Resume):
    """
    Analyze a resume and provide optimization suggestions
    
    Returns:
    - Resume quality score
    - Identified strengths
    - Areas for improvement
    - ATS optimization suggestions
    """
    try:
        logger.info(f"Analyzing resume: {resume.resume_id}")
        
        # Validate and optimize resume
        optimizer_tool = ResumeOptimizerTool()
        analysis = optimizer_tool._run(resume.resume_text, {})
        
        # Store in vector database
        vector_db.add_resume(
            resume.resume_id,
            resume.candidate_name,
            resume.resume_text,
            resume.metadata
        )
        
        return {
            "resume_id": resume.resume_id,
            "candidate_name": resume.candidate_name,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error analyzing resume: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/v1/resumes/upload")
async def upload_resume(resume: Resume):
    """Upload a resume to the system"""
    try:
        resume_id = vector_db.add_resume(
            resume.resume_id,
            resume.candidate_name,
            resume.resume_text,
            resume.metadata
        )
        
        return {
            "success": True,
            "resume_id": resume_id,
            "message": "Resume uploaded successfully"
        }
    except Exception as e:
        logger.error(f"Error uploading resume: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


# ==================== Matching Endpoints ====================

@app.post("/api/v1/match/job-to-resumes")
async def find_matching_resumes(job_id: str, job_text: str, top_k: int = 5):
    """
    Find resumes that match a job description
    
    Returns:
    - List of matching resumes with similarity scores
    - Match confidence
    """
    try:
        logger.info(f"Finding resumes matching job: {job_id}")
        
        matches = vector_db.find_matching_resumes(job_text, top_k=top_k)
        
        return {
            "job_id": job_id,
            "matches_found": len(matches),
            "matches": [
                {
                    "id": m["id"],
                    "score": 1 - m["score"],  # Convert distance to similarity
                    "metadata": m["metadata"],
                    "preview": m["document"]
                }
                for m in matches
            ],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error finding matching resumes: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/v1/match/resume-to-jobs")
async def find_matching_jobs(resume_id: str, resume_text: str, top_k: int = 5):
    """
    Find job descriptions that match a resume
    
    Returns:
    - List of matching jobs with similarity scores
    - Match confidence
    """
    try:
        logger.info(f"Finding jobs matching resume: {resume_id}")
        
        matches = vector_db.find_matching_jobs(resume_text, top_k=top_k)
        
        return {
            "resume_id": resume_id,
            "matches_found": len(matches),
            "matches": [
                {
                    "id": m["id"],
                    "score": 1 - m["score"],  # Convert distance to similarity
                    "metadata": m["metadata"],
                    "preview": m["document"]
                }
                for m in matches
            ],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error finding matching jobs: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


# ==================== Comprehensive Analysis Endpoint ====================

@app.post("/api/v1/hiring/analyze")
async def analyze_hiring_request(job: JobDescription, resume: Resume):
    """
    Comprehensive hiring analysis combining job parsing and resume optimization
    
    Returns:
    - Complete job analysis
    - Resume optimization report
    - Overall match score (0-100)
    - Hiring recommendations
    """
    try:
        logger.info(f"Processing hiring request: job={job.job_id}, resume={resume.resume_id}")
        
        # Analyze job description
        jd_tool = JDParsingTool()
        jd_analysis = jd_tool._run(job.job_text)
        
        # Analyze and optimize resume
        validation_tool = ResomeValidationTool()
        resume_analysis = validation_tool._run(resume.resume_text, jd_analysis)
        
        # Store both in vector database
        vector_db.add_job_description(job.job_id, job.job_title, job.job_text, job.metadata)
        vector_db.add_resume(resume.resume_id, resume.candidate_name, resume.resume_text, resume.metadata)
        
        # Calculate match score
        match_score = resume_analysis.get("overall_match_score", 0)
        
        return {
            "job_id": job.job_id,
            "resume_id": resume.resume_id,
            "jd_analysis": jd_analysis,
            "resume_analysis": resume_analysis,
            "match_score": match_score,
            "recommendation": "STRONG MATCH" if match_score >= 75 else "GOOD MATCH" if match_score >= 60 else "FAIR" if match_score >= 40 else "NEEDS IMPROVEMENT",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in hiring analysis: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


# ==================== Admin Endpoints ====================

@app.get("/api/v1/admin/clear-db")
async def clear_database():
    """Clear all data from vector database (use with caution!)"""
    try:
        vector_db.clear_collection()
        return {
            "success": True,
            "message": "Database cleared successfully"
        }
    except Exception as e:
        logger.error(f"Error clearing database: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/admin/export")
async def export_database(filename: str = "vector_db_export.json"):
    """Export vector database to JSON file"""
    try:
        output_path = vector_db.export_data(filename)
        return {
            "success": True,
            "export_path": output_path,
            "message": "Database exported successfully"
        }
    except Exception as e:
        logger.error(f"Error exporting database: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Root Endpoint ====================

@app.get("/")
async def root():
    """Root endpoint with API documentation"""
    return {
        "name": "AI Hiring Assistant API",
        "version": "0.1.0",
        "description": "CrewAI-powered API for job description parsing and resume optimization",
        "endpoints": {
            "health": "/health",
            "stats": "/stats",
            "job_analysis": "POST /api/v1/jobs/analyze",
            "resume_analysis": "POST /api/v1/resumes/analyze",
            "hiring_analysis": "POST /api/v1/hiring/analyze",
            "find_matching_resumes": "POST /api/v1/match/job-to-resumes",
            "find_matching_jobs": "POST /api/v1/match/resume-to-jobs",
            "documentation": "/docs"
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )
