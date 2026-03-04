"""
Custom HR and Recruitment Agents using CrewAI
"""

from crewai import Agent, Task, Crew
from crewai_tools import BaseTool
from src.tools.custom_tools import JDParsingTool, ResomeValidationTool, ResumeOptimizerTool
from typing import Optional
import os


class JDParserAgent:
    """Agent specialized in parsing job descriptions"""
    
    def __init__(self):
        self.jd_parser_tool = JDParsingTool()
        self.agent = Agent(
            role="Senior Hiring Manager",
            goal="Parse and extract key requirements from job descriptions with high accuracy",
            backstory="""You are an experienced hiring manager with 15+ years of experience 
            in recruitment and talent acquisition. You excel at identifying key requirements, 
            skills, and qualifications from job descriptions. You understand what makes a 
            strong candidate profile and can articulate requirements clearly.""",
            tools=[self.jd_parser_tool],
            memory=True,
            verbose=True
        )
    
    def parse_job_description(self, job_description: str) -> dict:
        """Parse a job description and return structured requirements"""
        task = Task(
            description=f"""Analyze the following job description and extract all key requirements:
            
            {job_description}
            
            Provide:
            1. Job title
            2. Required skills (technical and soft)
            3. Required experience level
            4. Key responsibilities
            5. Nice-to-have qualifications
            6. Salary range if mentioned""",
            agent=self.agent,
            expected_output="Structured JSON with extracted job requirements"
        )
        
        # Run the task
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            verbose=True
        )
        
        result = crew.kickoff()
        return result


class ResumeOptimizerAgent:
    """Agent specialized in resume optimization and matching"""
    
    def __init__(self):
        self.resume_validator = ResomeValidationTool()
        self.resume_optimizer = ResumeOptimizerTool()
        self.agent = Agent(
            role="Career Coach and Resume Expert",
            goal="Optimize resumes to maximize job match scores and improve hiring chances",
            backstory="""You are a veteran career coach with extensive experience in helping 
            professionals advance their careers. You understand ATS systems, resume formatting, 
            keyword optimization, and what hiring managers look for. You've successfully helped 
            over 1000 candidates land their dream jobs by optimizing their application materials.""",
            tools=[self.resume_validator, self.resume_optimizer],
            memory=True,
            verbose=True
        )
    
    def optimize_resume(self, resume_text: str, job_description: str) -> dict:
        """Optimize a resume against a job description"""
        task = Task(
            description=f"""Analyze and optimize the following resume for the given job:
            
            RESUME:
            {resume_text}
            
            JOB DESCRIPTION:
            {job_description}
            
            Provide:
            1. Overall match score (0-100)
            2. Matched skills and missing skills
            3. Top 5 recommendations for improvement
            4. Suggested resume format improvements
            5. Keywords to add for ATS optimization
            6. Estimated hiring probability with improvements""",
            agent=self.agent,
            expected_output="Detailed resume optimization report with actionable recommendations"
        )
        
        # Run the task
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            verbose=True
        )
        
        result = crew.kickoff()
        return result


class HiringAssistantCrew:
    """Complete crew for hiring assistance combining JD Parser and Resume Optimizer"""
    
    def __init__(self):
        self.jd_parser_agent = JDParserAgent()
        self.resume_optimizer_agent = ResumeOptimizerAgent()
    
    def process_hiring_request(self, job_description: str, resume_text: str) -> dict:
        """Process a complete hiring request: parse JD and optimize resume"""
        
        # Step 1: Parse the job description
        jd_analysis = self.jd_parser_agent.parse_job_description(job_description)
        
        # Step 2: Optimize resume against JD
        resume_optimization = self.resume_optimizer_agent.optimize_resume(resume_text, job_description)
        
        return {
            "job_description_analysis": jd_analysis,
            "resume_optimization": resume_optimization,
            "timestamp": __import__("datetime").datetime.now().isoformat()
        }


# Factory functions for easy agent creation
def create_jd_parser_agent() -> Agent:
    """Create a JD Parser agent"""
    return JDParserAgent().agent


def create_resume_optimizer_agent() -> Agent:
    """Create a Resume Optimizer agent"""
    return ResumeOptimizerAgent().agent
