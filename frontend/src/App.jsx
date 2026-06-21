import React, { useState } from 'react';
import './App.css';
import ResumeAnalyzer from './components/ResumeAnalyzer';

function App() {
  return (
    <div className="App">
      <header className="app-header">
        <h1>Resume Analyzer</h1>
        <p>AI-Powered Resume Analysis using Google Gemini</p>
      </header>
      <main>
        <ResumeAnalyzer />
      </main>
    </div>
  );
}

export default App;
