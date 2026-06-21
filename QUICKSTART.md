# Resume Analyzer - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Setup Your API Key
1. Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. In the `backend` folder, create a `.env` file (copy from `.env.example`):
   ```
   GEMINI_API_KEY=your_key_here
   ```

### Step 2: Install Dependencies

#### Backend (Python)
```bash
cd backend
pip install -r requirements.txt
```

#### Frontend (Node.js)
```bash
cd frontend
npm install
```

### Step 3: Run the Application

#### Option A: Using VS Code Terminal

**Terminal 1 - Backend:**
- Run the task: `Ctrl+Shift+B` → Select "Start Backend Server"
- Or manually: `cd backend && python -m uvicorn app.main:app --reload`

**Terminal 2 - Frontend:**
- Run the task: `Ctrl+Shift+B` → Select "Start Frontend Dev Server"
- Or manually: `cd frontend && npm run dev`

#### Option B: Manual Commands

**Terminal 1:**
```bash
cd backend
python -m uvicorn app.main:app --reload
```

**Terminal 2:**
```bash
cd frontend
npm run dev
```

### Step 4: Open Application
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📝 How to Use

1. **Paste your resume** into the text area
2. **Click "Analyze Resume"**
3. **View results:**
   - Professional score (1-100)
   - Detailed analysis
   - Key strengths
   - Improvement suggestions

## 🛠️ Project Structure

```
Resume Analyzer/
├── backend/              # FastAPI server
│   ├── app/
│   │   ├── main.py       # Main API
│   │   ├── models.py     # Data models
│   │   └── services/
│   │       └── gemini_service.py  # AI integration
│   └── requirements.txt
├── frontend/             # React + Vite
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── styles/       # CSS files
│   │   └── App.jsx       # Main component
│   └── package.json
└── README.md
```

## 🔌 API Reference

### POST /api/analyze
```json
{
  "resume_text": "John Doe\n..."
}
```

**Response:**
```json
{
  "analysis": "...",
  "score": 85,
  "strengths": ["..."],
  "improvements": ["..."],
  "summary": "..."
}
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Backend error | Check `.env` has GEMINI_API_KEY |
| Port already in use | Kill process or change port |
| npm not found | Install Node.js from nodejs.org |
| Python not found | Install Python from python.org |

## 📚 Next Steps

- Customize the UI in `frontend/src/components/`
- Add more analysis features in `backend/app/services/`
- Deploy to production
- Add file upload support
- Implement caching

---

**Need help?** Check the full README.md for detailed documentation.
