from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.models import ResumeAnalysisRequest, ResumeAnalysisResponse
from app.services.gemini_service import GeminiService

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Resume Analyzer API",
    description="API for analyzing resumes using Google Gemini",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini service
gemini_service = GeminiService()

@app.get("/")
async def root():
    return {
        "message": "Resume Analyzer API",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "/api/analyze",
            "health": "/health"
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/api/analyze", response_model=ResumeAnalysisResponse)
async def analyze_resume(request: ResumeAnalysisRequest):
    """
    Analyze a resume and return comprehensive feedback.
    
    Args:
        request: ResumeAnalysisRequest containing resume text
    
    Returns:
        ResumeAnalysisResponse with analysis, score, strengths, and improvements
    """
    result = gemini_service.analyze_resume(request.resume_text)
    
    return ResumeAnalysisResponse(
        analysis=result.get("analysis", ""),
        score=float(result.get("score", 50)),
        strengths=result.get("strengths", []),
        improvements=result.get("improvements", []),
        summary=result.get("summary", "")
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
