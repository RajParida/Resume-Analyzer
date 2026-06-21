import os
import json
from typing import Dict, Any
import google.generativeai as genai

class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-pro")

    def analyze_resume(self, resume_text: str) -> Dict[str, Any]:
        prompt = f"""Analyze the following resume and provide:
1. A detailed analysis of the resume
2. A score from 1-100 based on professionalism, clarity, and content quality
3. Key strengths (list 3-5)
4. Areas for improvement (list 3-5)
5. A brief summary

Resume:
{resume_text}

Please provide the response in the following JSON format:
{{
    "analysis": "detailed analysis text",
    "score": 85,
    "strengths": ["strength1", "strength2", "strength3"],
    "improvements": ["improvement1", "improvement2", "improvement3"],
    "summary": "brief summary"
}}"""

        response = self.model.generate_content(prompt)
        
        try:
            # Extract JSON from response
            response_text = response.text
            # Try to find JSON in the response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                result = json.loads(json_str)
            else:
                result = json.loads(response_text)
            return result
        except json.JSONDecodeError:
            return {
                "analysis": response.text,
                "score": 50,
                "strengths": ["Unable to parse detailed analysis"],
                "improvements": ["Please try again with a clearer resume format"],
                "summary": "Analysis completed but parsing failed"
            }
