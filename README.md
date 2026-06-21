# Resume Analyzer

A full-stack web application that uses Google's Gemini API to intelligently analyze and evaluate resumes. Get comprehensive feedback on your resume including a professional score, key strengths, and actionable improvement suggestions.

## 🌟 Features

- **AI-Powered Analysis**: Uses Google Gemini API for intelligent resume analysis
- **Comprehensive Scoring**: Get a professional score from 1-100
- **Strengths Identification**: Automatic detection of resume strengths
- **Improvement Suggestions**: Actionable recommendations for resume enhancement
- **User-Friendly Interface**: Clean, responsive React interface
- **Real-time Feedback**: Instant analysis with detailed insights
- **CORS Enabled**: Easy frontend-backend communication

## 🛠️ Tech Stack

### Frontend
- **React 18**: UI library
- **Vite**: Modern build tool
- **Axios**: HTTP client
- **CSS3**: Responsive styling

### Backend
- **FastAPI**: Python web framework
- **Uvicorn**: ASGI server
- **Google Generative AI**: Gemini API integration
- **Pydantic**: Data validation

## 📋 Prerequisites

- Node.js 18+ and npm
- Python 3.9+
- Google Gemini API key (get it from [Google AI Studio](https://makersuite.google.com/app/apikey))

## 🚀 Quick Start

### 1. Setup Environment Variables

Create a `.env` file in the `backend` folder:

```bash
cd backend
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 2. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Install Frontend Dependencies

```bash
cd frontend
npm install
```

## 🏃 Running the Project

### Start the Backend Server

```bash
cd backend
python -m uvicorn app.main:app --reload
```

The backend API will be available at `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

### Start the Frontend Development Server

In a new terminal:

```bash
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:5173`

## 📁 Project Structure

```
Resume Analyzer/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI application
│   │   ├── models.py         # Pydantic models
│   │   └── services/
│   │       └── gemini_service.py  # Gemini API integration
│   ├── requirements.txt
│   ├── pyproject.toml
│   ├── .env.example
│   └── .gitignore
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ResumeAnalyzer.jsx
│   │   │   └── AnalysisResult.jsx
│   │   ├── styles/
│   │   │   ├── ResumeAnalyzer.css
│   │   │   └── AnalysisResult.css
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── .gitignore
│   └── README.md
├── .github/
│   └── copilot-instructions.md
├── .gitignore
└── README.md
```

## 🔌 API Endpoints

### Analyze Resume
- **Endpoint**: `POST /api/analyze`
- **Description**: Analyzes a resume using the Gemini API

**Request:**
```json
{
  "resume_text": "John Doe\n...(resume content)..."
}
```

**Response:**
```json
{
  "analysis": "Detailed analysis of the resume...",
  "score": 85,
  "strengths": [
    "Strong technical background",
    "Clear career progression",
    "Excellent communication skills"
  ],
  "improvements": [
    "Add more quantifiable achievements",
    "Include relevant certifications",
    "Expand on project contributions"
  ],
  "summary": "This is a well-structured resume with strong technical credentials..."
}
```

### Health Check
- **Endpoint**: `GET /health`
- **Response**: `{ "status": "healthy" }`

### Root
- **Endpoint**: `GET /`
- **Response**: API information and available endpoints

## 💡 How to Use

1. **Enter Your Resume**: Paste your resume text into the text area
2. **Analyze**: Click the "Analyze Resume" button
3. **Review Results**: 
   - See your professional score (displayed in a circle)
   - Read the detailed analysis
   - Review identified strengths
   - Check improvement suggestions
4. **Iterate**: Make improvements and re-analyze

## 🔒 Security Notes

- The `.env` file is in `.gitignore` to prevent exposing your API key
- Never commit your `.env` file to version control
- Use environment variables for sensitive information
- CORS is configured to accept requests from localhost during development

## 📦 Building for Production

### Build Frontend
```bash
cd frontend
npm run build
```

This creates optimized production files in `frontend/dist/`

### Production Backend
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🐛 Troubleshooting

### Backend Connection Error
- Ensure the backend server is running (`python -m uvicorn app.main:app --reload`)
- Check if port 8000 is available
- Verify CORS is enabled in the backend

### Gemini API Error
- Verify your API key is correct in `.env`
- Check that you have API quota available
- Ensure the Google Generative AI library is installed: `pip install google-generativeai`

### Frontend Not Loading
- Ensure Node.js is installed: `node --version`
- Clear npm cache: `npm cache clean --force`
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`

## 📚 Documentation

- [Gemini API Documentation](https://ai.google.dev/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Feel free to fork the project and submit pull requests.

## ✨ Future Enhancements

- File upload support (PDF, DOCX)
- Resume template suggestions
- Comparison with job descriptions
- Multiple resume analysis
- Export analysis results
- Dark mode
- Internationalization (i18n)

## 📧 Support

For issues or questions, please open an issue on GitHub.

---

**Happy resume analyzing! 🚀**
