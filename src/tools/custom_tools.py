"""
Custom tools for HR and recruitment assistant tasks
"""

import json
import re
from typing import Any, Optional
from crewai_tools import BaseTool


class JDParsingTool(BaseTool):
    """Tool for parsing and extracting structured information from Job Descriptions"""
    
    name: str = "JD_Parser"
    description: str = "Parses job descriptions and extracts key information such as required skills, experience, qualifications, and responsibilities"
    
    def _run(self, job_description: str) -> dict:
        """
        Parse job description and extract structured information
        """
        # Keywords mapping
        skill_keywords = [
            'python', 'javascript', 'java', 'cpp', 'csharp', 'go', 'rust', 'typescript',
            'sql', 'mongodb', 'postgresql', 'django', 'flask', 'fastapi', 'react', 'vue',
            'angular', 'kubernetes', 'docker', 'aws', 'gcp', 'azure', 'git', 'linux',
            'agile', 'scrum', 'ci/cd', 'machine learning', 'tensorflow', 'pytorch',
            'nlp', 'computer vision', 'data analysis', 'tableau', 'power bi'
        ]
        
        experience_pattern = r'(\d+)\+?\s*(?:years?|yrs?)'
        
        # Convert to lowercase for analysis
        jd_lower = job_description.lower()
        
        # Extract skills
        found_skills = []
        for skill in skill_keywords:
            if re.search(rf'\b{skill}\b', jd_lower):
                found_skills.append(skill)
        
        # Extract experience
        experience_matches = re.findall(experience_pattern, jd_lower)
        min_experience = int(min(experience_matches)) if experience_matches else 0
        
        # Extract salary if present
        salary_pattern = r'\$(\d+,?\d*)\s*(?:k|K)?'
        salary_matches = re.findall(salary_pattern, job_description)
        
        # Extract job title
        title_pattern = r'^(.*?)\n'
        title = re.search(title_pattern, job_description)
        
        result = {
            "title": title.group(1).strip() if title else "Unknown",
            "required_skills": found_skills,
            "minimum_experience_years": min_experience,
            "salary_range": salary_matches if salary_matches else None,
            "raw_analysis": {
                "total_words": len(job_description.split()),
                "total_lines": len(job_description.split('\n'))
            }
        }
        
        return result


class ResomeValidationTool(BaseTool):
    """Tool for validating and scoring resumes against job requirements"""
    
    name: str = "Resume_Validator"
    description: str = "Validates resume against job requirements and provides a match score"
    
    def _run(self, resume_text: str, jd_requirements: dict) -> dict:
        """
        Validate resume against job description requirements
        """
        resume_lower = resume_text.lower()
        
        # Check for required skills
        required_skills = jd_requirements.get("required_skills", [])
        matched_skills = []
        missing_skills = []
        
        for skill in required_skills:
            if re.search(rf'\b{skill}\b', resume_lower):
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)
        
        # Calculate match score
        skill_match_percentage = (len(matched_skills) / len(required_skills) * 100) if required_skills else 0
        
        # Check for experience
        experience_pattern = r'(\d+)\+?\s*(?:years?|yrs?)'
        experience_matches = re.findall(experience_pattern, resume_lower)
        max_experience = int(max(experience_matches)) if experience_matches else 0
        
        required_experience = jd_requirements.get("minimum_experience_years", 0)
        experience_match = max_experience >= required_experience
        
        # Overall scoring
        overall_score = (skill_match_percentage * 0.7) + (100 if experience_match else 50)
        
        result = {
            "skill_match_percentage": round(skill_match_percentage, 2),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "experience_match": experience_match,
            "candidate_experience": max_experience,
            "required_experience": required_experience,
            "overall_match_score": round(overall_score / 1.7, 2)  # Normalize to 0-100
        }
        
        return result


class ResumeOptimizerTool(BaseTool):
    """Tool for suggesting resume improvements based on job requirements"""
    
    name: str = "Resume_Optimizer"
    description: str = "Suggests improvements to resume to better match job requirements and improve ATS compatibility"
    
    def _run(self, resume_text: str, jd_requirements: dict) -> dict:
        """
        Provide optimization suggestions for resume
        """
        suggestions = []
        priority_improvements = []
        
        # Check for missing skills
        missing_skills = jd_requirements.get("missing_skills", [])
        if missing_skills:
            priority_improvements.append({
                "type": "Add Skills",
                "priority": "HIGH",
                "suggestion": f"Add the following skills to your resume: {', '.join(missing_skills)}",
                "impact": "Can significantly improve match score"
            })
        
        # Check for experience gap
        required_experience = jd_requirements.get("required_experience_years", 0)
        candidate_experience = jd_requirements.get("candidate_experience", 0)
        if candidate_experience < required_experience:
            gap = required_experience - candidate_experience
            suggestions.append({
                "type": "Experience Gap",
                "priority": "MEDIUM",
                "suggestion": f"You have {candidate_experience} years of experience but {required_experience} years are required. Consider highlighting transferable skills or related projects.",
                "impact": "May require justification in cover letter"
            })
        
        # Check for ATS keywords
        if len(resume_text.split(',')) < 10:
            suggestions.append({
                "type": "Keyword Optimization",
                "priority": "MEDIUM",
                "suggestion": "Use more industry-specific keywords and technical terms from the job description",
                "impact": "Better ATS (Applicant Tracking System) compatibility"
            })
        
        # Check formatting
        if len(resume_text.split('\n')) < 5:
            suggestions.append({
                "type": "Formatting",
                "priority": "LOW",
                "suggestion": "Use clear section headers (Skills, Experience, Education) for better readability",
                "impact": "Improves human readability"
            })
        
        result = {
            "total_suggestions": len(priority_improvements) + len(suggestions),
            "priority_improvements": priority_improvements,
            "additional_suggestions": suggestions,
            "optimization_score": min(100, 70 + len(priority_improvements) * 5)
        }
        
        return result
