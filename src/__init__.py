"""
AI Hiring Assistant with CrewAI
Multi-agent system for job parsing and resume optimization
"""

__version__ = "0.1.0"
__author__ = "AI Hiring Assistant Contributors"
__description__ = "Intelligent hiring assistant powered by CrewAI"

from src.agents.hiring_agents import HiringAssistantCrew, JDParserAgent, ResumeOptimizerAgent

__all__ = [
    "HiringAssistantCrew",
    "JDParserAgent",
    "ResumeOptimizerAgent",
]
