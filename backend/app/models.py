from pydantic import BaseModel
from typing import List, Optional

class ResumeAnalysisRequest(BaseModel):
    resume_text: str

class ResumeAnalysisResponse(BaseModel):
    analysis: str
    score: float
    strengths: List[str]
    improvements: List[str]
    summary: str
