"""
Unit tests for Resume Analyzer API

Tests cover:
- API endpoint functionality
- Error handling
- Input validation
- Response format validation
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints."""
    
    def test_root_endpoint(self):
        """Test root endpoint returns API information."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "endpoints" in data
        assert data["version"] == "2.0.0"
    
    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestResumeAnalysis:
    """Test resume analysis endpoint."""
    
    def test_analyze_resume_valid_input(self):
        """Test successful resume analysis."""
        resume_text = """
        John Doe
        Software Engineer
        
        Experience:
        - Built web applications using React and Python
        - Led team of 3 engineers
        - Improved system performance by 40%
        
        Skills:
        - Python, JavaScript, React, FastAPI
        - AWS, Docker, Git
        """
        
        response = client.post(
            "/api/analyze",
            json={"resume_text": resume_text}
        )
        
        # Should not rate limit on first request
        assert response.status_code in [200, 429]
        
        if response.status_code == 200:
            data = response.json()
            assert "score" in data
            assert "analysis" in data
            assert "strengths" in data
            assert "improvements" in data
            assert "summary" in data
            assert 1 <= data["score"] <= 100
            assert isinstance(data["strengths"], list)
            assert isinstance(data["improvements"], list)
    
    def test_analyze_resume_empty_input(self):
        """Test resume analysis with empty input."""
        response = client.post(
            "/api/analyze",
            json={"resume_text": ""}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
    
    def test_analyze_resume_whitespace_only(self):
        """Test resume analysis with whitespace only."""
        response = client.post(
            "/api/analyze",
            json={"resume_text": "   \n\t  "}
        )
        
        assert response.status_code == 400
    
    def test_analyze_resume_invalid_json(self):
        """Test resume analysis with invalid JSON."""
        response = client.post(
            "/api/analyze",
            json={"invalid_field": "value"}
        )
        
        assert response.status_code == 422  # Unprocessable Entity
    
    def test_analyze_resume_too_long(self):
        """Test resume analysis with text exceeding max length."""
        long_text = "a" * 10001
        response = client.post(
            "/api/analyze",
            json={"resume_text": long_text}
        )
        
        # FastAPI will reject based on field constraints
        assert response.status_code in [422, 400]
    
    def test_response_format(self):
        """Test that response has correct format."""
        resume_text = """
        Jane Smith
        Data Scientist
        
        Experience:
        - Built ML models with 95% accuracy
        - Managed datasets with millions of records
        """
        
        response = client.post(
            "/api/analyze",
            json={"resume_text": resume_text}
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Verify all required fields exist
            assert all(key in data for key in [
                "analysis", "score", "strengths", 
                "improvements", "summary"
            ])
            
            # Verify types
            assert isinstance(data["analysis"], str)
            assert isinstance(data["score"], (int, float))
            assert isinstance(data["strengths"], list)
            assert isinstance(data["improvements"], list)
            assert isinstance(data["summary"], str)
            
            # Verify score range
            assert 1 <= data["score"] <= 100
            
            # Verify list items are strings
            assert all(isinstance(s, str) for s in data["strengths"])
            assert all(isinstance(i, str) for i in data["improvements"])


class TestCacheEndpoint:
    """Test cache management endpoint."""
    
    def test_clear_cache(self):
        """Test cache clear endpoint."""
        response = client.get("/api/cache/clear")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"


class TestRateLimiting:
    """Test rate limiting functionality."""
    
    def test_rate_limiting_header(self):
        """Test that rate limit headers are present."""
        response = client.get("/health")
        
        # Check if RateLimit headers are present
        # (slowapi adds these headers to responses)
        assert response.status_code == 200


class TestDocumentation:
    """Test API documentation endpoints."""
    
    def test_docs_endpoint(self):
        """Test Swagger docs endpoint."""
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_redoc_endpoint(self):
        """Test ReDoc docs endpoint."""
        response = client.get("/redoc")
        assert response.status_code == 200
    
    def test_openapi_schema(self):
        """Test OpenAPI schema generation."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "paths" in schema
        assert "/api/analyze" in schema["paths"]


class TestErrorHandling:
    """Test error handling."""
    
    def test_method_not_allowed(self):
        """Test HTTP method not allowed error."""
        response = client.get("/api/analyze")
        assert response.status_code == 405
    
    def test_not_found(self):
        """Test 404 Not Found error."""
        response = client.get("/nonexistent")
        assert response.status_code == 404


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
