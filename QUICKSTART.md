# Quick Start Guide

## Initial Setup

1. **Install Python dependencies:**
```powershell
pip install -r requirements.txt
```

2. **Install Playwright browsers:**
```powershell
playwright install chromium
```

3. **Configure environment variables:**
   - Copy `.env.example` to `.env`
   - Edit `.env` and add your:
     - `OPENAI_API_KEY`
     - `EMAIL` (your student email)
     - `SECRET` (your secret string)

## Testing Locally

### Test individual components:
```powershell
# Test browser automation
python test.py browser

# Test LLM integration
python test.py llm

# Test with demo quiz
python test.py demo
```

### Run the API server:
```powershell
python main.py
```

Server will start at `http://localhost:8000`

### Send a test request:
```powershell
# Using curl (if available)
curl -X POST http://localhost:8000/quiz -H "Content-Type: application/json" -d '{\"email\":\"your@email.com\",\"secret\":\"your_secret\",\"url\":\"https://tds-llm-analysis.s-anand.net/demo\"}'

# Or using PowerShell:
$body = @{
    email = "your@email.com"
    secret = "your_secret"
    url = "https://tds-llm-analysis.s-anand.net/demo"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/quiz" -Method POST -Body $body -ContentType "application/json"
```

## Deployment Options

### Option 1: ngrok (Quick & Easy)
1. Download ngrok from https://ngrok.com/
2. Start your server: `python main.py`
3. In another terminal: `ngrok http 8000`
4. Use the HTTPS URL from ngrok for your submission

### Option 2: Cloud Platform
- **Render.com** (Free tier available)
- **Railway.app** (Free tier available)
- **Heroku** (Paid)
- **AWS/GCP/Azure** (Various pricing)

### Option 3: Own Server
- Set up a VPS (DigitalOcean, Linode, etc.)
- Install Python and dependencies
- Use systemd or supervisor to run as service
- Configure nginx as reverse proxy for HTTPS

## Google Form Submission

Fill out the form with:
1. **Email**: Your student email
2. **Secret**: A unique string (save in `.env`)
3. **System Prompt** (≤100 chars): See `PROMPTS.md` for examples
4. **User Prompt** (≤100 chars): See `PROMPTS.md` for examples
5. **API Endpoint**: Your deployed server URL (HTTPS preferred)
6. **GitHub Repo**: Your public repo URL with MIT LICENSE

## During Evaluation (Sat 29 Nov 2025, 3:00-4:00 PM IST)

- Ensure your server is running and accessible
- Monitor logs for incoming requests
- Server must respond within 3 minutes
- Keep your internet connection stable

## Troubleshooting

### "Module not found" errors
```powershell
pip install -r requirements.txt
```

### "Playwright browser not found"
```powershell
playwright install chromium
```

### "OpenAI API error"
- Check your API key in `.env`
- Verify you have credits in your OpenAI account

### Server not receiving requests
- Check firewall settings
- Verify your endpoint URL is correct
- Test with curl/Postman first

### Timeout errors
- Increase `TIMEOUT_SECONDS` in `.env`
- Optimize LLM prompts for faster responses
- Consider using faster GPT models

## Tips for Success

1. **Test thoroughly** with the demo endpoint
2. **Handle errors gracefully** - retries are allowed
3. **Keep prompts concise** - LLM should respond quickly
4. **Monitor costs** - OpenAI API usage during testing
5. **Version control** - Commit working versions frequently
6. **Backup plan** - Have secondary deployment ready

## Common Quiz Task Types

Based on the project description, prepare for:
- **Web scraping**: Extracting data from HTML/JavaScript pages
- **API calls**: Fetching data from REST APIs
- **PDF processing**: Extracting tables/text from PDFs
- **Data analysis**: Aggregations, statistics, filtering
- **Visualization**: Creating charts and graphs
- **Text processing**: Cleaning, parsing, transformation

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Playwright Python](https://playwright.dev/python/)
- [OpenAI API](https://platform.openai.com/docs/)
- [Pandas Documentation](https://pandas.pydata.org/)
