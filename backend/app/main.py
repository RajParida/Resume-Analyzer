"""
Resume Analyzer API

A FastAPI application that analyzes resumes using Google's Gemini AI API.
Provides endpoints for resume analysis with caching and rate limiting.
"""

import logging
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv
from app.models import ResumeAnalysisRequest, ResumeAnalysisResponse
from app.services.gemini_service import GeminiService, GeminiServiceError

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Resume Analyzer API",
    description="AI-powered resume analysis using Google Gemini",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini service
try:
    gemini_service = GeminiService()
    logger.info("Application started successfully")
except GeminiServiceError as e:
    logger.error(f"Failed to initialize Gemini service: {str(e)}")
    raise


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    """Handle rate limit exceeded errors."""
    logger.warning(f"Rate limit exceeded for {get_remote_address(request)}")
    return HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail="Too many requests. Please try again later."
    )


@app.get("/", tags=["Health"])
async def root():
    """
    Root endpoint providing API information.
    
    Returns:
        Dictionary with API metadata and available endpoints
    """
    logger.info("Root endpoint accessed")
    return {
        "message": "Resume Analyzer API",
        "version": "2.0.0",
        "description": "AI-powered resume analysis using Google Gemini",
        "endpoints": {
            "analyze": "/api/analyze",
            "health": "/health",
            "docs": "/docs"
        }
    }


@app.get("/health", tags=["Health"])
async def health():
    """
    Health check endpoint.
    
    Returns:
        Dictionary with service status
    """
    return {"status": "healthy", "service": "Resume Analyzer API"}


@app.post(
    "/api/analyze",
    response_model=ResumeAnalysisResponse,
    status_code=status.HTTP_200_OK,
    tags=["Analysis"],
    summary="Analyze a resume",
    description="Analyzes a resume and returns comprehensive feedback including score, strengths, and improvements."
)
@limiter.limit("10/minute")
async def analyze_resume(request, resume_request: ResumeAnalysisRequest):
    """
    Analyze a resume and return comprehensive feedback.
    
    Args:
        resume_request: ResumeAnalysisRequest containing resume text
    
    Returns:
        ResumeAnalysisResponse with analysis, score, strengths, and improvements
        
    Raises:
        HTTPException: If analysis fails
        
    Example:
        POST /api/analyze
        {
            "resume_text": "John Doe\nSoftware Engineer..."
        }
    """
    try:
        logger.info(f"Resume analysis requested (length: {len(resume_request.resume_text)} chars)")
        
        # Validate input
        if not resume_request.resume_text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Resume text cannot be empty"
            )
        
        # Perform analysis
        result = gemini_service.analyze_resume(resume_request.resume_text)
        
        logger.info(f"Analysis completed successfully (score: {result['score']})")
        
        return ResumeAnalysisResponse(
            analysis=result.get("analysis", ""),
            score=float(result.get("score", 50)),
            strengths=result.get("strengths", []),
            improvements=result.get("improvements", []),
            summary=result.get("summary", ""),
            timestamp=result.get("timestamp", "")
        )
        
    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except GeminiServiceError as e:
        logger.error(f"Gemini service error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Failed to analyze resume. Please try again later."
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later."
        )


@app.get("/api/cache/clear", tags=["Admin"])
async def clear_cache():
    """
    Clear the analysis cache (admin endpoint).
    
    Returns:
        Dictionary with cache clear status
    """
    try:
        gemini_service.clear_cache()
        logger.info("Cache cleared by admin")
        return {"status": "success", "message": "Analysis cache cleared"}
    except Exception as e:
        logger.error(f"Error clearing cache: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to clear cache"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
