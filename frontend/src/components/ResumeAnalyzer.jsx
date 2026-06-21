import React, { useState } from 'react';
import axios from 'axios';
import '../styles/ResumeAnalyzer.css';
import AnalysisResult from './AnalysisResult';

const ResumeAnalyzer = () => {
  const [resumeText, setResumeText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleAnalyze = async () => {
    if (!resumeText.trim()) {
      setError('Please enter resume text');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await axios.post('http://localhost:8000/api/analyze', {
        resume_text: resumeText
      });
      setResult(response.data);
    } catch (err) {
      setError(
        err.response?.data?.detail || 
        'Failed to analyze resume. Please make sure the backend is running.'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setResumeText('');
    setResult(null);
    setError('');
  };

  return (
    <div className="resume-analyzer">
      <div className="input-section">
        <h2>Enter Your Resume</h2>
        <textarea
          value={resumeText}
          onChange={(e) => setResumeText(e.target.value)}
          placeholder="Paste your resume text here..."
          className="resume-input"
          disabled={loading}
        />
        <div className="button-group">
          <button 
            onClick={handleAnalyze} 
            disabled={loading || !resumeText.trim()}
            className="btn btn-primary"
          >
            {loading ? 'Analyzing...' : 'Analyze Resume'}
          </button>
          <button 
            onClick={handleClear}
            disabled={loading}
            className="btn btn-secondary"
          >
            Clear
          </button>
        </div>
      </div>

      {error && (
        <div className="error-message">
          <p>{error}</p>
        </div>
      )}

      {result && <AnalysisResult result={result} />}
    </div>
  );
};

export default ResumeAnalyzer;
