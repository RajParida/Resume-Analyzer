"""
Pydantic models for Resume Analyzer API

Defines request and response schemas for the API endpoints.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class ResumeAnalysisRequest(BaseModel):
    """
    Request model for resume analysis endpoint.
    
    Attributes:
        resume_text: The resume content as plain text (max 10000 characters)
    """
    resume_text: str = Field(
        ...,
        min_length=10,
        max_length=10000,
        description="Resume content as plain text",
        example="John Doe\nSoftware Engineer\nExperience:\n..."
    )

    class Config:
        json_schema_extra = {
            "example": {
                "resume_text": "John Doe\nSoftware Engineer with 5 years of experience..."
            }
        }


class ResumeAnalysisResponse(BaseModel):
    """
    Response model for resume analysis endpoint.
    
    Attributes:
        analysis: Detailed analysis of the resume
        score: Professional score from 1-100
        strengths: List of key strengths identified
        improvements: List of areas for improvement
        summary: Brief summary of the analysis
        timestamp: When the analysis was performed
    """
    analysis: str = Field(
        ...,
        description="Detailed analysis of the resume"
    )
    score: float = Field(
        ...,
        ge=1,
        le=100,
        description="Professional score from 1 to 100"
    )
    strengths: List[str] = Field(
        ...,
        description="List of identified strengths",
        min_items=1,
        max_items=5
    )
    improvements: List[str] = Field(
        ...,
        description="List of areas for improvement",
        min_items=1,
        max_items=5
    )
    summary: str = Field(
        ...,
        description="Brief summary of the analysis"
    )
    timestamp: Optional[str] = Field(
        None,
        description="ISO format timestamp of when analysis was performed"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "analysis": "This resume demonstrates...",
                "score": 85,
                "strengths": ["Strong technical background", "Clear career progression"],
                "improvements": ["Add more metrics", "Highlight leadership"],
                "summary": "Well-structured resume with good content",
                "timestamp": "2024-01-15T10:30:00"
            }
        }
