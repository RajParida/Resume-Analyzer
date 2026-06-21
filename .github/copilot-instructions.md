# Resume Analyzer - Development Guide

## Project Overview
Resume Analyzer is a full-stack web application that uses the Gemini API to analyze and evaluate resumes. It consists of:
- **Frontend**: React application with Vite bundler
- **Backend**: FastAPI server with Gemini API integration

## Development Setup

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+
- Gemini API key

### Environment Variables

Create a `.env` file in the `backend` folder:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

## Running the Project

### Backend
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`
The backend API will be available at `http://localhost:8000`

## Project Structure

```
Resume Analyzer/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   └── services/
│   │       └── gemini_service.py
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Key Features
- Resume upload and parsing
- AI-powered resume analysis using Gemini API
- Real-time feedback and suggestions
- Professional scoring and recommendations

## API Endpoints

### POST /api/analyze
Analyzes a resume using the Gemini API.

**Request:**
```json
{
  "resume_text": "string"
}
```

**Response:**
```json
{
  "analysis": "string",
  "score": number,
  "strengths": ["string"],
  "improvements": ["string"]
}
```
