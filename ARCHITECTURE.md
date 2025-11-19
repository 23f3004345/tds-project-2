# LLM Analysis Quiz - Project Summary

## What This Project Does

This application automatically solves data analysis quizzes using LLMs. It:

1. **Receives quiz tasks** via API endpoint
2. **Fetches quiz pages** using browser automation (Playwright)
3. **Downloads required data files** (PDFs, CSVs, etc.)
4. **Analyzes data** using GPT models
5. **Submits answers** to evaluation endpoint
6. **Chains through multiple quizzes** until completion

## Architecture

```
┌─────────────┐
│   Client    │
│  (Evaluator)│
└──────┬──────┘
       │ POST /quiz
       │ {email, secret, url}
       ▼
┌─────────────────┐
│   FastAPI       │
│   Server        │
│   (main.py)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Quiz Solver    │
│ (quiz_solver.py)│
└─┬───────────┬───┘
  │           │
  ▼           ▼
┌──────┐  ┌──────┐
│Browser│  │ LLM  │
│Handler│  │Handler│
└───┬───┘  └───┬──┘
    │          │
    ▼          ▼
┌────────┐ ┌──────┐
│Playwright│ │OpenAI│
└──────────┘ └──────┘
```

## Key Components

### 1. `main.py` - FastAPI Server
- Handles incoming POST requests
- Validates email/secret
- Spawns quiz solving tasks
- Returns 200/403/400 responses

### 2. `quiz_solver.py` - Core Logic
- Orchestrates the quiz-solving process
- Manages quiz chains (multiple URLs)
- Handles 3-minute time limit
- Retries on failures

### 3. `browser_handler.py` - Web Automation
- Uses Playwright for JavaScript rendering
- Fetches quiz pages
- Downloads data files
- Extracts content

### 4. `llm_handler.py` - AI Integration
- Interfaces with OpenAI GPT models
- Solves data analysis tasks
- Extracts structured answers
- Analyzes data files

### 5. `data_processor.py` - Data Handling
- Processes PDFs, CSVs, Excel files
- Extracts and summarizes data
- Creates visualizations
- Performs aggregations

### 6. `config.py` - Configuration
- Loads environment variables
- Manages settings
- Creates directories

## Quiz Solving Flow

```
1. Receive POST /quiz
   ↓
2. Validate credentials
   ↓
3. Start quiz solver (async)
   ↓
4. Fetch quiz page with browser
   ↓
5. Extract task instructions
   ↓
6. Download any required files
   ↓
7. Analyze data with LLM
   ↓
8. Extract final answer
   ↓
9. Submit to endpoint
   ↓
10. Check response:
    - Correct? → Next URL or done
    - Wrong? → Retry or next
   ↓
11. Repeat until:
    - No more URLs
    - Time limit (3 min)
    - Error
```

## Supported Task Types

- ✅ **Web Scraping**: Extract data from HTML/JavaScript pages
- ✅ **Data Download**: Fetch PDFs, CSVs, Excel files
- ✅ **PDF Processing**: Extract text and tables from PDFs
- ✅ **Data Analysis**: Sum, mean, filter, group, aggregate
- ✅ **Visualization**: Generate charts as base64 images
- ✅ **Text Processing**: Clean, parse, transform text
- ✅ **API Calls**: Fetch data from REST APIs
- ✅ **JSON Handling**: Parse and extract from JSON

## API Endpoints

### `POST /quiz`
Receive and process quiz task

**Request:**
```json
{
  "email": "student@example.com",
  "secret": "secret_string",
  "url": "https://example.com/quiz-123"
}
```

**Response:**
```json
{
  "status": "accepted",
  "message": "Quiz solving started for https://example.com/quiz-123"
}
```

### `GET /`
Health check

**Response:**
```json
{
  "status": "running",
  "service": "LLM Analysis Quiz Solver"
}
```

### `GET /health`
Health check endpoint

## Environment Variables

Required in `.env`:
- `OPENAI_API_KEY` - Your OpenAI API key
- `EMAIL` - Your student email
- `SECRET` - Your secret string
- `PORT` - Server port (default: 8000)
- `HOST` - Server host (default: 0.0.0.0)
- `MODEL` - GPT model to use (default: gpt-4-turbo-preview)
- `TIMEOUT_SECONDS` - Max time per quiz chain (default: 180)

## Security Features

- ✅ Secret validation (403 on mismatch)
- ✅ Email validation
- ✅ JSON validation (400 on invalid)
- ✅ Environment variable protection
- ✅ No secrets in code/git
- ✅ Error handling
- ✅ Timeout protection

## Testing

```powershell
# Test browser
python test.py browser

# Test LLM
python test.py llm

# Test with demo quiz
python test.py demo

# Run server
python main.py

# Test endpoint
$body = @{
    email = "your@email.com"
    secret = "your_secret"
    url = "https://tds-llm-analysis.s-anand.net/demo"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/quiz" -Method POST -Body $body -ContentType "application/json"
```

## Deployment Options

1. **Render.com** (Recommended)
   - Free tier with HTTPS
   - Easy GitHub integration
   - Automatic deploys

2. **Railway.app**
   - Free $5 credit/month
   - Simple setup
   - Good for small projects

3. **ngrok**
   - Local development
   - Quick testing
   - Free tier limitations

4. **Heroku/DigitalOcean**
   - More control
   - Paid options
   - Production-ready

## Project Structure

```
TDS PROJECT2/
├── main.py                 # FastAPI server
├── quiz_solver.py          # Quiz solving logic
├── browser_handler.py      # Playwright automation
├── llm_handler.py          # OpenAI integration
├── data_processor.py       # Data processing
├── config.py               # Configuration
├── test.py                 # Testing utilities
├── requirements.txt        # Python dependencies
├── .env.example            # Environment template
├── .env                    # Your credentials (not in git)
├── .gitignore             # Git ignore rules
├── Procfile               # For Heroku/Render
├── runtime.txt            # Python version
├── setup.ps1              # Setup script
├── README.md              # Project overview
├── QUICKSTART.md          # Quick start guide
├── DEPLOYMENT.md          # Deployment guide
├── PROMPTS.md             # Prompt strategies
├── LICENSE                # MIT License
└── ARCHITECTURE.md        # This file
```

## Dependencies

- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **Playwright** - Browser automation
- **OpenAI** - LLM API
- **Pandas** - Data analysis
- **PyPDF2** - PDF processing
- **Matplotlib** - Visualization
- **aiohttp** - Async HTTP client
- **BeautifulSoup4** - HTML parsing

## Limitations & Considerations

1. **Time Limit**: 3 minutes per quiz chain
2. **File Size**: JSON payloads under 1MB
3. **Token Limits**: LLM context windows
4. **API Costs**: OpenAI charges per token
5. **Free Tier Limits**: Platform-specific constraints
6. **Browser Resources**: Playwright needs RAM
7. **Network**: Requires stable internet

## Future Enhancements

Potential improvements:
- [ ] Multi-model support (Claude, Gemini)
- [ ] Caching for repeated queries
- [ ] Parallel quiz solving
- [ ] Enhanced error recovery
- [ ] Detailed logging/monitoring
- [ ] Unit tests
- [ ] Rate limiting
- [ ] Queue system for requests
- [ ] WebSocket for real-time updates
- [ ] Dashboard for monitoring

## Performance Tips

1. **Model Selection**: Use GPT-3.5 for simple tasks, GPT-4 for complex
2. **Prompt Engineering**: Keep prompts concise and specific
3. **Data Chunking**: Process large files in chunks
4. **Caching**: Cache LLM responses for similar queries
5. **Async Processing**: Already implemented for concurrency
6. **Resource Management**: Close browser when done

## Troubleshooting

### Common Issues

1. **Playwright not found**: Run `playwright install chromium`
2. **OpenAI API errors**: Check API key and credits
3. **Timeout errors**: Increase `TIMEOUT_SECONDS`
4. **Memory issues**: Use smaller models or chunk data
5. **Port conflicts**: Change `PORT` in `.env`
6. **403 Errors**: Verify email/secret match `.env`

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## License

MIT License - See LICENSE file

## Support

For issues:
1. Check logs
2. Review QUICKSTART.md
3. Test components individually
4. Verify environment variables
5. Check OpenAI API status

## Evaluation Checklist

Before evaluation day:
- [ ] Server deployed and accessible
- [ ] HTTPS endpoint working
- [ ] Demo quiz solves successfully
- [ ] GitHub repo public with MIT license
- [ ] Google Form submitted
- [ ] Environment variables configured
- [ ] OpenAI credits sufficient
- [ ] Logs accessible
- [ ] Backup deployment ready
- [ ] Internet connection tested

## Scoring Components

1. **Prompt Testing**: System vs User prompts
2. **API Quiz Solving**: Correct answers submitted
3. **Viva**: Design choices explained

Good luck! 🚀
