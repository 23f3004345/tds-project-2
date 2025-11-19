# Project Completion Checklist

## Phase 1: Initial Setup ✓

- [x] Project structure created
- [x] All Python files created
- [x] Dependencies listed in requirements.txt
- [x] Configuration system implemented
- [x] Environment template created (.env.example)
- [x] Git ignore configured

## Phase 2: Development (Your Tasks)

### Environment Configuration
- [ ] Create `.env` file from `.env.example`
- [ ] Add your OpenAI API key
- [ ] Add your student email
- [ ] Choose and set a secret string
- [ ] Verify all environment variables

### Local Testing
- [ ] Install Python dependencies
  ```powershell
  pip install -r requirements.txt
  ```
- [ ] Install Playwright browsers
  ```powershell
  playwright install chromium
  ```
- [ ] Test browser component
  ```powershell
  python test.py browser
  ```
- [ ] Test LLM component
  ```powershell
  python test.py llm
  ```
- [ ] Test with demo quiz
  ```powershell
  python test.py demo
  ```
- [ ] Start server locally
  ```powershell
  python main.py
  ```
- [ ] Test endpoint with PowerShell
  ```powershell
  $body = @{email="your@email.com"; secret="your_secret"; url="https://tds-llm-analysis.s-anand.net/demo"} | ConvertTo-Json
  Invoke-RestMethod -Uri "http://localhost:8000/quiz" -Method POST -Body $body -ContentType "application/json"
  ```

### Code Review & Customization
- [ ] Review all Python files
- [ ] Understand the architecture (read ARCHITECTURE.md)
- [ ] Customize if needed (timeouts, models, etc.)
- [ ] Add any additional features you want
- [ ] Test changes thoroughly

## Phase 3: Prompt Engineering

### System Prompt (Defense)
- [ ] Read PROMPTS.md for strategies
- [ ] Write your system prompt (≤100 chars)
- [ ] Test locally with various attacks
- [ ] Refine based on testing
- [ ] Finalize system prompt

**Your System Prompt:**
```
_____________________________________________________________________________
```

### User Prompt (Attack)
- [ ] Read PROMPTS.md for strategies
- [ ] Write your user prompt (≤100 chars)
- [ ] Test locally against various defenses
- [ ] Refine based on testing
- [ ] Finalize user prompt

**Your User Prompt:**
```
_____________________________________________________________________________
```

## Phase 4: GitHub Setup

### Repository Creation
- [ ] Create new GitHub repository
- [ ] Initialize git in project folder
  ```powershell
  git init
  git add .
  git commit -m "Initial commit"
  ```
- [ ] Add remote and push
  ```powershell
  git remote add origin https://github.com/yourusername/your-repo.git
  git branch -M main
  git push -u origin main
  ```

### Repository Configuration
- [ ] Verify LICENSE file is present (MIT)
- [ ] Ensure `.env` is NOT committed
- [ ] Update README with your info
- [ ] Make repository PUBLIC
- [ ] Add repository description
- [ ] Add relevant topics/tags

**Your GitHub Repo URL:**
```
https://github.com/_________________/___________________
```

## Phase 5: Deployment

### Choose Platform
- [ ] Decided on platform (Render/Railway/ngrok/Other)
- [ ] Created account on chosen platform

### Render.com (Recommended)
- [ ] Connected GitHub repository
- [ ] Created new Web Service
- [ ] Configured build command:
  ```
  pip install -r requirements.txt && playwright install chromium --with-deps
  ```
- [ ] Configured start command:
  ```
  python main.py
  ```
- [ ] Added environment variables:
  - [ ] OPENAI_API_KEY
  - [ ] EMAIL
  - [ ] SECRET
  - [ ] PORT (8000)
  - [ ] HOST (0.0.0.0)
  - [ ] MODEL (gpt-4-turbo-preview)
  - [ ] PLAYWRIGHT_BROWSERS_PATH (/ms-playwright)
- [ ] Deployed successfully
- [ ] Verified deployment status

### OR Railway.app
- [ ] Connected GitHub repository
- [ ] Created new project
- [ ] Added environment variables
- [ ] Generated domain
- [ ] Deployed successfully

### OR ngrok
- [ ] Downloaded and installed ngrok
- [ ] Started local server
- [ ] Started ngrok tunnel
- [ ] Got HTTPS URL

**Your Deployment URL:**
```
https://_________________________________________________/quiz
```

## Phase 6: Testing Deployment

### Health Check
- [ ] Test health endpoint
  ```powershell
  Invoke-RestMethod -Uri "https://your-url/health"
  ```
- [ ] Verify returns `{"status": "healthy"}`

### Security Testing
- [ ] Test with wrong secret (should return 403)
  ```powershell
  $body = @{email="your@email.com"; secret="wrong_secret"; url="https://tds-llm-analysis.s-anand.net/demo"} | ConvertTo-Json
  Invoke-RestMethod -Uri "https://your-url/quiz" -Method POST -Body $body -ContentType "application/json"
  ```
- [ ] Test with invalid JSON (should return 400)
- [ ] Test with wrong email (should return 403)

### Functional Testing
- [ ] Test with correct credentials
  ```powershell
  $body = @{email="your@email.com"; secret="your_secret"; url="https://tds-llm-analysis.s-anand.net/demo"} | ConvertTo-Json
  Invoke-RestMethod -Uri "https://your-url/quiz" -Method POST -Body $body -ContentType "application/json"
  ```
- [ ] Verify returns accepted status
- [ ] Check logs for quiz solving process
- [ ] Verify demo quiz completes successfully
- [ ] Test multiple times to ensure consistency

### Performance Testing
- [ ] Check response time (<30s initial response)
- [ ] Verify quiz completes within 3 minutes
- [ ] Monitor resource usage on platform
- [ ] Check OpenAI API usage/costs

## Phase 7: Google Form Submission

### Pre-Submission Verification
- [ ] Local testing passed ✓
- [ ] Deployment successful ✓
- [ ] Demo quiz solves correctly ✓
- [ ] GitHub repo public with LICENSE ✓
- [ ] All documentation complete ✓
- [ ] Prompts finalized ✓

### Form Fields Ready
- [ ] Email address: _________________________________
- [ ] Secret string: _________________________________
- [ ] System prompt (≤100 chars): ___________________
- [ ] User prompt (≤100 chars): _____________________
- [ ] API endpoint: https://________________________/quiz
- [ ] GitHub repo: https://github.com/______________/_______

### Submit Form
- [ ] Double-check all fields
- [ ] Verify URLs are correct (test again!)
- [ ] Submit Google Form
- [ ] Save confirmation/receipt
- [ ] Note submission timestamp

**Submission Date/Time:**
```
____________________
```

## Phase 8: Pre-Evaluation Preparation

### Server Verification (Day Before)
- [ ] Check server is running
- [ ] Test health endpoint
- [ ] Run demo quiz test
- [ ] Review logs for any errors
- [ ] Verify OpenAI credits sufficient (~$5-10)
- [ ] Check platform status (no maintenance)

### Backup Plan
- [ ] Have secondary deployment ready (if using ngrok)
- [ ] Know how to quickly restart server
- [ ] Have OpenAI API key backup
- [ ] Save backup of .env file
- [ ] Document quick recovery steps

### Viva Preparation
- [ ] Review ARCHITECTURE.md
- [ ] Understand your code flow
- [ ] Prepare to explain design choices:
  - [ ] Why this architecture?
  - [ ] How does LLM integration work?
  - [ ] What's your error handling strategy?
  - [ ] How do you handle different data types?
  - [ ] What about security?
- [ ] Test microphone and speakers
- [ ] Ensure stable internet connection

## Phase 9: Evaluation Day (Sat 29 Nov 2025, 3:00-4:00 PM IST)

### Morning Checklist
- [ ] Server status verified
- [ ] Health endpoint responding
- [ ] Demo quiz test passed
- [ ] Logs accessible
- [ ] Internet connection stable
- [ ] Computer/laptop fully charged
- [ ] Phone backup ready

### 30 Minutes Before (2:30 PM IST)
- [ ] Final server check
- [ ] Final demo quiz test
- [ ] Clear any logs for fresh start
- [ ] Open log monitoring
- [ ] Close unnecessary applications
- [ ] Silence phone notifications

### During Evaluation (3:00-4:00 PM IST)
- [ ] Monitor server logs actively
- [ ] Don't modify code
- [ ] Keep deployment dashboard open
- [ ] Have backup ready
- [ ] Be prepared for viva call
- [ ] Take notes of any issues

### Post-Evaluation
- [ ] Review server logs
- [ ] Check submission results (if provided)
- [ ] Document lessons learned
- [ ] Thank you're evaluators 😊

## Phase 10: Post-Project

### Cleanup (Optional)
- [ ] Stop/pause free tier services if not needed
- [ ] Review and reduce OpenAI costs
- [ ] Archive project documentation

### Learning Review
- [ ] What worked well?
- [ ] What would you improve?
- [ ] What did you learn about LLMs?
- [ ] What did you learn about deployment?

## Additional Resources Checklist

### Documentation Read
- [ ] README.md
- [ ] QUICKSTART.md
- [ ] DEPLOYMENT.md
- [ ] SUBMISSION.md
- [ ] PROMPTS.md
- [ ] ARCHITECTURE.md

### External Resources
- [ ] FastAPI documentation reviewed
- [ ] Playwright documentation reviewed
- [ ] OpenAI API documentation reviewed
- [ ] Deployment platform documentation reviewed

## Notes & Observations

### Issues Encountered:
```
_____________________________________________________________________________
_____________________________________________________________________________
_____________________________________________________________________________
```

### Solutions Found:
```
_____________________________________________________________________________
_____________________________________________________________________________
_____________________________________________________________________________
```

### Improvements Made:
```
_____________________________________________________________________________
_____________________________________________________________________________
_____________________________________________________________________________
```

---

## Quick Command Reference

```powershell
# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Test components
python test.py browser
python test.py llm
python test.py demo

# Run server
python main.py

# Test endpoint
$body = @{email="your@email.com"; secret="your_secret"; url="https://tds-llm-analysis.s-anand.net/demo"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/quiz" -Method POST -Body $body -ContentType "application/json"

# Git commands
git add .
git commit -m "your message"
git push origin main
```

---

**Progress Tracker:**
- Phase 1: ✓ Complete (provided)
- Phase 2: ⬜ Your task
- Phase 3: ⬜ Your task
- Phase 4: ⬜ Your task
- Phase 5: ⬜ Your task
- Phase 6: ⬜ Your task
- Phase 7: ⬜ Your task
- Phase 8: ⬜ Your task
- Phase 9: ⬜ Future
- Phase 10: ⬜ Future

**Good luck with your project! 🚀**
