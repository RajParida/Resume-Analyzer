import React, { useState } from 'react';
import axios from 'axios';
import '../styles/ResumeAnalyzer.css';
import AnalysisResult from './AnalysisResult';

/**
 * ResumeAnalyzer Component
 * 
 * Main component for resume input and analysis.
 * Handles user input, API communication, and error management.
 */
const ResumeAnalyzer = () => {
  const [resumeText, setResumeText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const API_BASE_URL = 'http://localhost:8000';
  const MIN_RESUME_LENGTH = 10;
  const MAX_RESUME_LENGTH = 10000;

  /**
   * Validates resume text before submission.
   * @returns {string|null} Error message if validation fails, null otherwise
   */
  const validateResume = (text) => {
    if (!text.trim()) {
      return 'Please enter resume text';
    }
    if (text.length < MIN_RESUME_LENGTH) {
      return `Resume must be at least ${MIN_RESUME_LENGTH} characters`;
    }
    if (text.length > MAX_RESUME_LENGTH) {
      return `Resume cannot exceed ${MAX_RESUME_LENGTH} characters`;
    }
    return null;
  };

  /**
   * Handles resume analysis API call.
   */
  const handleAnalyze = async () => {
    // Validate input
    const validationError = validateResume(resumeText);
    if (validationError) {
      setError(validationError);
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      console.log('Sending resume for analysis...');
      const response = await axios.post(`${API_BASE_URL}/api/analyze`, {
        resume_text: resumeText
      }, {
        timeout: 30000 // 30 second timeout
      });

      console.log('Analysis completed:', response.data);
      setResult(response.data);
    } catch (err) {
      console.error('Analysis error:', err);
      
      // Provide user-friendly error messages
      let errorMessage = 'Failed to analyze resume. ';
      
      if (err.response?.status === 429) {
        errorMessage += 'Too many requests. Please wait a moment before trying again.';
      } else if (err.response?.status === 400) {
        errorMessage += err.response.data?.detail || 'Invalid resume format.';
      } else if (err.response?.status === 503) {
        errorMessage += 'Analysis service is temporarily unavailable. Please try again later.';
      } else if (err.code === 'ECONNABORTED') {
        errorMessage += 'Request timed out. Please try with a shorter resume.';
      } else if (err.message === 'Network Error') {
        errorMessage += 'Make sure the backend server is running on http://localhost:8000';
      } else {
        errorMessage += err.response?.data?.detail || err.message;
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Clears all input and results.
   */
  const handleClear = () => {
    setResumeText('');
    setResult(null);
    setError('');
  };

  /**
   * Handles text area changes.
   */
  const handleTextChange = (e) => {
    const text = e.target.value;
    setResumeText(text);
    
    // Clear error if user starts typing
    if (error && text.trim()) {
      setError('');
    }
  };

  return (
    <div className="resume-analyzer">
      <div className="input-section">
        <h2>Enter Your Resume</h2>
        <p className="input-hint">
          Paste your resume text here (minimum 10 characters, maximum 10,000)
        </p>
        
        <textarea
          value={resumeText}
          onChange={handleTextChange}
          placeholder="Paste your resume text here..."
          className="resume-input"
          disabled={loading}
          maxLength={MAX_RESUME_LENGTH}
        />
        
        <div className="character-count">
          {resumeText.length} / {MAX_RESUME_LENGTH} characters
        </div>

        <div className="button-group">
          <button 
            onClick={handleAnalyze} 
            disabled={loading || !resumeText.trim()}
            className="btn btn-primary"
            title={!resumeText.trim() ? 'Enter resume text to analyze' : 'Analyze resume'}
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Analyzing...
              </>
            ) : (
              'Analyze Resume'
            )}
          </button>
          <button 
            onClick={handleClear}
            disabled={loading}
            className="btn btn-secondary"
            title="Clear input and results"
          >
            Clear
          </button>
        </div>
      </div>

      {error && (
        <div className="error-message" role="alert">
          <svg className="error-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          <p>{error}</p>
        </div>
      )}

      {result && <AnalysisResult result={result} />}
    </div>
  );
};

export default ResumeAnalyzer;
