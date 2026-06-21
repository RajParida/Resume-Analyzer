import React from 'react';
import '../styles/AnalysisResult.css';

const AnalysisResult = ({ result }) => {
  const getScoreColor = (score) => {
    if (score >= 80) return '#28a745'; // Green
    if (score >= 60) return '#ffc107'; // Yellow
    return '#dc3545'; // Red
  };

  return (
    <div className="analysis-result">
      <h2>Analysis Results</h2>
      
      <div className="score-section">
        <div className="score-circle" style={{ borderColor: getScoreColor(result.score) }}>
          <span className="score-value" style={{ color: getScoreColor(result.score) }}>
            {result.score}
          </span>
          <span className="score-label">/100</span>
        </div>
      </div>

      <div className="summary-section">
        <h3>Summary</h3>
        <p>{result.summary}</p>
      </div>

      <div className="analysis-section">
        <h3>Detailed Analysis</h3>
        <p>{result.analysis}</p>
      </div>

      <div className="strengths-weaknesses">
        <div className="strengths">
          <h3>Strengths</h3>
          <ul>
            {result.strengths.map((strength, index) => (
              <li key={index}>{strength}</li>
            ))}
          </ul>
        </div>

        <div className="improvements">
          <h3>Areas for Improvement</h3>
          <ul>
            {result.improvements.map((improvement, index) => (
              <li key={index}>{improvement}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default AnalysisResult;
