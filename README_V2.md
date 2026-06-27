# Resume Analyzer - Production Grade

A production-ready full-stack web application that uses Google's Gemini API to intelligently analyze and evaluate resumes. Enterprise-grade features for internship and career readiness.

**Version 2.0** - Enhanced with unit tests, rate limiting, caching, and comprehensive documentation.

## ⭐ Key Features

### AI-Powered Analysis
- ✅ Google Gemini API integration
- ✅ Professional scoring system (1-100)
- ✅ Automatic strengths identification
- ✅ Actionable improvement recommendations
- ✅ Detailed professional feedback

### Production-Ready Backend
- ✅ **30+ Unit Tests** with comprehensive coverage
- ✅ **Rate Limiting** (10 requests/minute per IP)
- ✅ **Intelligent Caching** (LRU cache, 1-hour TTL)
- ✅ **Error Handling** with user-friendly messages
- ✅ **Full Type Hints** for code safety
- ✅ **Structured Logging** for debugging
- ✅ **Auto-generated API Documentation** (Swagger/OpenAPI)
- ✅ **Input Validation** with Pydantic

### Modern Frontend
- ✅ React 18 with hooks
- ✅ Vite for fast development
- ✅ Responsive design (mobile/tablet/desktop)
- ✅ Real-time character counter
- ✅ Loading states with animations
- ✅ Professional UI with gradients

## 🛠️ Tech Stack

### Frontend
- **React 18** - Modern UI framework
- **Vite 5** - Lightning-fast bundler
- **Axios** - HTTP client
- **CSS3** - Responsive styling

### Backend
- **FastAPI** - Modern Python framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation & type hints
- **Google Generative AI** - Gemini API
- **SlowAPI** - Rate limiting
- **Cachetools** - Intelligent caching

## 📋 Prerequisites

- **Python 3.9+**
- **Node.js 18+** and npm
- **Google Gemini API Key** - [Get it here](https://makersuite.google.com/app/apikey)

## 🚀 Quick Start

### 1. Setup Environment Variables

Create `.env` in the `backend` folder:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

### 2. Install Dependencies

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### 3. Start Servers

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 4. Access Application

- **Frontend**: http://localhost:5173
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📊 Project Structure

```
Resume Analyzer/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI with logging & rate limiting
│   │   ├── models.py         # Pydantic models with validation
│   │   └── services/
│   │       └── gemini_service.py  # Gemini integration, caching
│   ├── tests/
│   │   └── test_api.py       # 30+ comprehensive tests
│   ├── requirements.txt
│   ├── .env.example
│   └── .pylintrc
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ResumeAnalyzer.jsx
│   │   │   └── AnalysisResult.jsx
│   │   ├── styles/
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
│
└── .github/copilot-instructions.md
```

## 🔌 API Endpoints

### POST `/api/analyze` - Analyze Resume

**Request:**
```json
{
  "resume_text": "John Doe\nSoftware Engineer\n..."
}
```

**Response (200 OK):**
```json
{
  "analysis": "Detailed analysis...",
  "score": 85,
  "strengths": ["strength1", "strength2"],
  "improvements": ["improve1", "improve2"],
  "summary": "Brief summary...",
  "timestamp": "2024-01-15T10:30:00"
}
```

### GET `/health` - Health Check
```json
{ "status": "healthy" }
```

### GET `/docs` - API Documentation
Interactive Swagger UI for all endpoints

## 🧪 Testing

### Run All Tests

```bash
cd backend
pytest -v
```

### Test Coverage

```bash
pytest --cov=app tests/ --cov-report=html
```

### Test Categories

- ✅ Health endpoints
- ✅ Resume analysis (valid & invalid inputs)
- ✅ Input validation & edge cases
- ✅ Error handling
- ✅ Response format validation
- ✅ Rate limiting
- ✅ API documentation

See [TESTING.md](TESTING.md) for detailed testing guide.

## 🔒 Security

- ✅ **Secrets Management**: Environment variables only
- ✅ **Input Validation**: Pydantic with constraints
- ✅ **Rate Limiting**: Prevents abuse
- ✅ **CORS**: Localhost-only in development
- ✅ **Type Safety**: Full type hints
- ✅ **Error Messages**: No sensitive data exposure

## ⚡ Performance

- **Response Caching**: LRU cache (128 items, 1-hour TTL)
- **Frontend Optimization**: Minified production builds
- **API Design**: Stateless endpoints
- **Database**: Optional (currently in-memory)

## 📈 Scalability Path

### Current (Single Instance)
- In-memory caching
- Stateless API
- Local file storage

### Production (Multi-Instance)
1. Redis for distributed caching
2. PostgreSQL for persistence
3. Message queue (Celery) for async jobs
4. Load balancer
5. Docker containerization
6. Kubernetes orchestration

## 🚀 Production Build

### Backend

```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend

```bash
cd frontend
npm run build
```

## 💼 Google Internship Readiness

This project demonstrates enterprise software engineering:

✅ **Production-Grade Code**
- Comprehensive error handling
- Type safety with type hints
- Extensive logging
- Input validation

✅ **Professional Testing**
- 30+ unit tests
- Edge case coverage
- Rate limiting tests
- API validation

✅ **Performance & Scalability**
- Intelligent caching
- Rate limiting
- Optimized builds
- Scaling-ready architecture

✅ **Security**
- Environment-based config
- Input sanitization
- CORS configuration
- Safe error messages

✅ **Documentation**
- API docs (auto-generated)
- Testing guide
- Code comments
- Deployment guide

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup
- **[TESTING.md](TESTING.md)** - Testing guide
- **[SETUP_COMPLETE.md](SETUP_COMPLETE.md)** - Project summary

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection refused | Verify backend is running |
| GEMINI_API_KEY not set | Create `.env` with your key |
| Port in use | Use different port: `--port 8001` |
| Tests fail | Run `pip install -r requirements.txt` |

## ✨ Future Enhancements

- [ ] File upload (PDF, DOCX)
- [ ] Job description comparison
- [ ] User authentication
- [ ] Resume database
- [ ] Export to PDF
- [ ] Dark mode

## 📄 License

MIT License - Open source and free to use.

---

**Production-ready Resume Analyzer. Built for Google internship excellence! 🚀**
