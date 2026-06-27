"""
Gemini API Service for Resume Analysis

This module provides integration with Google's Generative AI API (Gemini)
for analyzing resume text and providing structured feedback.
"""

import os
import json
import logging
from typing import Dict, Any
from datetime import datetime, timedelta
import google.generativeai as genai
import cachetools

logger = logging.getLogger(__name__)


class GeminiServiceError(Exception):
    """Custom exception for Gemini service errors."""
    pass


class GeminiService:
    """
    Service for analyzing resumes using Google's Gemini API.
    
    Provides caching and error handling for resume analysis operations.
    """
    
    # Cache to store analysis results (LRU cache with 128 items)
    _cache: cachetools.LRUCache = cachetools.LRUCache(maxsize=128)
    _cache_times: Dict[str, datetime] = {}
    _CACHE_TTL = timedelta(hours=1)
    
    def __init__(self):
        """Initialize Gemini service with API key from environment."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise GeminiServiceError(
                "GEMINI_API_KEY environment variable not set. "
                "Please configure it in .env file."
            )
        
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel("gemini-pro")
            logger.info("Gemini service initialized successfully")
        except Exception as e:
            raise GeminiServiceError(f"Failed to initialize Gemini API: {str(e)}")

    def _get_cache_key(self, resume_text: str) -> str:
        """Generate cache key from resume text hash."""
        import hashlib
        return hashlib.md5(resume_text.encode()).hexdigest()

    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached result is still valid."""
        if cache_key not in self._cache_times:
            return False
        return datetime.now() - self._cache_times[cache_key] < self._CACHE_TTL

    def analyze_resume(self, resume_text: str) -> Dict[str, Any]:
        """
        Analyze a resume and return comprehensive feedback.
        
        Args:
            resume_text: The resume content as plain text
            
        Returns:
            Dictionary containing:
                - analysis: Detailed analysis text
                - score: Professional score (1-100)
                - strengths: List of key strengths
                - improvements: List of improvement areas
                - summary: Brief summary
                - timestamp: When analysis was performed
                
        Raises:
            GeminiServiceError: If analysis fails
            ValueError: If resume_text is empty or invalid
        """
        # Input validation
        if not resume_text or not resume_text.strip():
            raise ValueError("Resume text cannot be empty")
        
        if len(resume_text) > 10000:
            raise ValueError("Resume text exceeds maximum length of 10000 characters")
        
        # Check cache first
        cache_key = self._get_cache_key(resume_text)
        if cache_key in self._cache and self._is_cache_valid(cache_key):
            logger.info(f"Cache hit for resume analysis (key: {cache_key[:8]}...)")
            return self._cache[cache_key]

        # Build detailed prompt for Gemini
        prompt = self._build_analysis_prompt(resume_text)
        
        try:
            # Call Gemini API
            logger.info("Calling Gemini API for resume analysis")
            response = self.model.generate_content(prompt)
            
            if not response.text:
                raise GeminiServiceError("Empty response from Gemini API")
            
            # Parse and validate response
            result = self._parse_response(response.text)
            result["timestamp"] = datetime.now().isoformat()
            
            # Cache the result
            self._cache[cache_key] = result
            self._cache_times[cache_key] = datetime.now()
            logger.info(f"Analysis completed and cached (score: {result['score']})")
            
            return result
            
        except GeminiServiceError:
            raise
        except Exception as e:
            error_msg = f"Gemini API error: {str(e)}"
            logger.error(error_msg)
            raise GeminiServiceError(error_msg)

    def _build_analysis_prompt(self, resume_text: str) -> str:
        """Build a detailed prompt for resume analysis."""
        return f"""Analyze the following resume professionally and provide:
1. A detailed analysis highlighting key aspects
2. A score from 1-100 based on:
   - Structure and formatting (20%)
   - Content quality and clarity (30%)
   - Experience relevance (25%)
   - Skills presentation (15%)
   - Achievements and impact (10%)
3. 3-5 key strengths
4. 3-5 areas for improvement
5. A brief summary (2-3 sentences)

Resume:
{resume_text}

IMPORTANT: Respond ONLY with valid JSON in this exact format:
{{
    "analysis": "detailed analysis text here",
    "score": 75,
    "strengths": ["strength1", "strength2", "strength3"],
    "improvements": ["improvement1", "improvement2", "improvement3"],
    "summary": "brief summary here"
}}"""

    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse and validate Gemini API response.
        
        Args:
            response_text: Raw response from Gemini API
            
        Returns:
            Validated analysis dictionary
            
        Raises:
            GeminiServiceError: If response cannot be parsed
        """
        try:
            # Extract JSON from response (may be wrapped in text)
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise GeminiServiceError("No JSON found in response")
            
            json_str = response_text[start_idx:end_idx]
            result = json.loads(json_str)
            
            # Validate required fields
            required_fields = {"analysis", "score", "strengths", "improvements", "summary"}
            if not required_fields.issubset(set(result.keys())):
                raise GeminiServiceError(
                    f"Missing required fields in response. Expected: {required_fields}"
                )
            
            # Validate score is in valid range
            score = result.get("score", 0)
            if not isinstance(score, (int, float)) or score < 1 or score > 100:
                result["score"] = 50
                logger.warning("Invalid score in response, using default")
            else:
                result["score"] = float(score)
            
            # Ensure lists have proper format
            result["strengths"] = result.get("strengths", [])[:5]
            result["improvements"] = result.get("improvements", [])[:5]
            
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {str(e)}")
            raise GeminiServiceError(f"Failed to parse Gemini response: {str(e)}")

    def clear_cache(self) -> None:
        """Clear all cached analysis results."""
        self._cache.clear()
        self._cache_times.clear()
        logger.info("Analysis cache cleared")
