# Testing Guide - Resume Analyzer

## Backend Testing (Python)

### Run All Tests

```bash
cd backend
pytest -v
```

### Run Specific Test Classes

```bash
# Health check tests
pytest tests/test_api.py::TestHealthEndpoints -v

# Resume analysis tests
pytest tests/test_api.py::TestResumeAnalysis -v

# Error handling tests
pytest tests/test_api.py::TestErrorHandling -v
```

### Run with Coverage Report

```bash
pytest --cov=app tests/ --cov-report=html
```

This generates a coverage report in `htmlcov/index.html`.

### Test Categories

1. **Health Endpoints**: Verify API health checks
2. **Resume Analysis**: Valid input, edge cases, error handling
3. **Input Validation**: Empty, whitespace, too long, invalid JSON
4. **Response Format**: Verify all required fields and types
5. **Rate Limiting**: Verify rate limit enforcement
6. **Documentation**: Verify API docs are accessible
7. **Error Handling**: HTTP error codes and messages

### Example Test Output

```
tests/test_api.py::TestHealthEndpoints::test_root_endpoint PASSED
tests/test_api.py::TestHealthEndpoints::test_health_endpoint PASSED
tests/test_api.py::TestResumeAnalysis::test_analyze_resume_valid_input PASSED
tests/test_api.py::TestResumeAnalysis::test_analyze_resume_empty_input PASSED
tests/test_api.py::TestResumeAnalysis::test_response_format PASSED
```

## API Manual Testing

### Using cURL

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test resume analysis
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "John Doe\nSoftware Engineer\nExperience:\n- 5 years of Python development\n- Led team of 3"
  }'
```

### Using Postman

1. Import API endpoints into Postman
2. POST to `http://localhost:8000/api/analyze`
3. Set Body to JSON:
```json
{
  "resume_text": "Your resume text here"
}
```

### Using Python Requests

```python
import requests

resume = """
John Doe
Software Engineer

Experience:
- Built scalable web applications
- Led development teams
- Improved system performance
"""

response = requests.post(
    "http://localhost:8000/api/analyze",
    json={"resume_text": resume}
)

print(response.json())
```

## Frontend Testing

### Manual UI Testing

1. **Valid Input**: Paste a sample resume and click Analyze
2. **Character Counter**: Verify character count updates
3. **Loading State**: Verify spinner appears during analysis
4. **Error Messages**: Test with empty input, server down
5. **Results Display**: Verify all results display correctly
6. **Responsive**: Test on mobile, tablet, desktop

### Test Cases

| Test Case | Input | Expected | Status |
|-----------|-------|----------|--------|
| Valid resume | Full resume text | Analysis displays | ✓ |
| Empty input | Empty string | Error message | ✓ |
| Whitespace only | "   " | Error message | ✓ |
| Server down | Valid input | Connection error | ✓ |
| Valid response | Sample resume | Score displayed | ✓ |

## Performance Testing

### Backend Performance

```bash
# Test under load (100 requests, 10 concurrent)
ab -n 100 -c 10 http://localhost:8000/health

# With ApacheBench
ab -n 1000 -c 50 -p data.json -T application/json http://localhost:8000/api/analyze
```

### Load Testing with Locust

Create `locustfile.py`:
```python
from locust import HttpUser, task

class ResumeAnalyzerUser(HttpUser):
    @task
    def analyze_resume(self):
        self.client.post("/api/analyze", json={
            "resume_text": "Sample resume..."
        })
```

Run:
```bash
locust -f locustfile.py --host=http://localhost:8000
```

## Security Testing

### Test API Security

```bash
# Test CORS
curl -H "Origin: http://example.com" http://localhost:8000/api/analyze

# Test rate limiting
for i in {1..15}; do
  curl -X POST http://localhost:8000/api/analyze \
    -d '{"resume_text": "test"}' \
    -H "Content-Type: application/json"
done
```

### Input Sanitization

- ✓ SQL injection: No database backend
- ✓ XSS: Input goes to LLM, not HTML
- ✓ Command injection: No system commands
- ✓ Large payload: Max 10,000 characters enforced

## CI/CD Testing

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - run: |
          pip install -r backend/requirements.txt
          pytest backend/tests/ -v
```

## Test Checklist

Before deployment, verify:

- [ ] All unit tests pass
- [ ] No failing integration tests
- [ ] Rate limiting works
- [ ] Error messages are user-friendly
- [ ] Response times acceptable
- [ ] No console errors in frontend
- [ ] Mobile responsive
- [ ] API documentation accurate

## Debugging Tests

### Verbose Output
```bash
pytest -vv tests/test_api.py
```

### Show Print Statements
```bash
pytest -s tests/test_api.py
```

### Stop on First Failure
```bash
pytest -x tests/test_api.py
```

### Run Last Failed
```bash
pytest --lf tests/test_api.py
```

## Common Issues

| Issue | Solution |
|-------|----------|
| "Connection refused" | Start backend server first |
| "Timeout" | Increase timeout in test |
| "Rate limited" | Wait between requests |
| "GEMINI_API_KEY not set" | Create `.env` file with key |
| "Import error" | Run `pip install -r requirements.txt` |

---

**For more help**, see [README.md](../README.md) and backend code comments.
