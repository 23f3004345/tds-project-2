# Deployment Guide

## Deploying to Render.com (Recommended - Free HTTPS)

### Step 1: Prepare Your Repository

1. Push all code to GitHub
2. Ensure `.env` is in `.gitignore` (it should be)
3. Commit all changes

### Step 2: Create Render Account

1. Go to https://render.com/
2. Sign up with GitHub
3. Authorize Render to access your repositories

### Step 3: Create Web Service

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `tds-quiz-solver` (or your choice)
   - **Environment**: `Python 3`
   - **Build Command**: 
     ```
     pip install -r requirements.txt && playwright install chromium --with-deps
     ```
   - **Start Command**: 
     ```
     python main.py
     ```
   - **Instance Type**: Free

### Step 4: Configure Environment Variables

In Render dashboard, add these environment variables:
- `OPENAI_API_KEY`: Your OpenAI API key
- `EMAIL`: Your student email
- `SECRET`: Your secret string
- `PORT`: 8000
- `HOST`: 0.0.0.0
- `PLAYWRIGHT_BROWSERS_PATH`: /ms-playwright

### Step 5: Deploy

1. Click "Create Web Service"
2. Wait for deployment (5-10 minutes first time)
3. Your service will be at: `https://your-service-name.onrender.com`

### Step 6: Test

```powershell
$body = @{
    email = "your@email.com"
    secret = "your_secret"
    url = "https://tds-llm-analysis.s-anand.net/demo"
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://your-service-name.onrender.com/quiz" -Method POST -Body $body -ContentType "application/json"
```

---

## Alternative: ngrok (Quick Local Testing)

### Advantages
- Quick setup
- Good for testing
- No cloud configuration needed

### Disadvantages
- URL changes on restart (free tier)
- Less reliable for production
- Must keep local machine running

### Steps

1. Download ngrok: https://ngrok.com/download
2. Extract and add to PATH
3. Start your local server:
   ```powershell
   python main.py
   ```
4. In another terminal:
   ```powershell
   ngrok http 8000
   ```
5. Use the HTTPS URL shown (e.g., `https://abc123.ngrok.io`)

---

## Alternative: Railway.app

### Steps

1. Go to https://railway.app/
2. Sign in with GitHub
3. "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Add environment variables (same as Render)
6. Railway will auto-detect Python and deploy
7. Click "Generate Domain" for public URL

---

## Alternative: Heroku

### Steps

1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Add buildpacks:
   ```powershell
   heroku buildpacks:add heroku/python
   heroku buildpacks:add https://github.com/mxschmitt/heroku-playwright-buildpack
   ```
5. Set config vars:
   ```powershell
   heroku config:set OPENAI_API_KEY=your_key
   heroku config:set EMAIL=your@email.com
   heroku config:set SECRET=your_secret
   ```
6. Create `Procfile`:
   ```
   web: python main.py
   ```
7. Deploy:
   ```powershell
   git push heroku main
   ```

---

## Alternative: DigitalOcean App Platform

### Steps

1. Sign up at https://www.digitalocean.com/
2. Go to App Platform
3. Create new app from GitHub
4. Select repository
5. Configure:
   - Type: Web Service
   - Environment Variables: Add all from `.env`
   - Build Command: `pip install -r requirements.txt && playwright install chromium`
   - Run Command: `python main.py`
6. Deploy

---

## Monitoring Your Deployment

### Check Health
```powershell
Invoke-RestMethod -Uri "https://your-url/health"
```

### View Logs (Render)
1. Go to your service dashboard
2. Click "Logs" tab
3. Monitor in real-time

### Test Quiz Endpoint
```powershell
$body = @{
    email = "your@email.com"
    secret = "your_secret"
    url = "https://tds-llm-analysis.s-anand.net/demo"
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://your-url/quiz" -Method POST -Body $body -ContentType "application/json"
```

---

## Security Best Practices

1. **Never commit `.env` file** - Already in `.gitignore`
2. **Use environment variables** - For all secrets
3. **HTTPS only** - Required for production
4. **Validate input** - Already implemented in code
5. **Rate limiting** - Consider adding for production
6. **Monitor costs** - OpenAI API usage

---

## Troubleshooting Deployment

### Playwright Installation Fails
Add to build command:
```
playwright install chromium --with-deps
```

### Port Binding Issues
Ensure `config.py` uses environment PORT:
```python
PORT = int(os.getenv("PORT", "8000"))
```

### Memory Issues (Free Tier)
- Use smaller models if possible
- Limit concurrent requests
- Optimize data processing

### Timeout on Long Tasks
- Increase timeout in platform settings
- Process tasks asynchronously
- Return 200 immediately, solve in background

---

## Before Evaluation Day

- [ ] Server deployed and accessible
- [ ] Test with demo endpoint successfully
- [ ] Environment variables configured
- [ ] Logs accessible for debugging
- [ ] HTTPS endpoint confirmed
- [ ] GitHub repo is public
- [ ] MIT LICENSE added to repo
- [ ] Google Form submitted
- [ ] Test secret validation (wrong secret returns 403)
- [ ] Monitor OpenAI API credits

---

## During Evaluation (3:00-4:00 PM IST, 29 Nov 2025)

1. **Keep laptop/system on** (if using ngrok)
2. **Monitor logs** for incoming requests
3. **Have backup plan** - Secondary deployment ready
4. **Check internet** - Stable connection essential
5. **OpenAI credits** - Ensure sufficient balance
6. **Don't modify code** - Once evaluation starts

---

## Cost Estimates

### Free Tier Options
- **Render**: Free tier includes 750 hours/month
- **Railway**: $5 free credit/month
- **ngrok**: Free tier with limitations

### OpenAI Costs (Approximate)
- GPT-4 Turbo: ~$0.01-0.03 per quiz (depending on complexity)
- GPT-3.5 Turbo: ~$0.001-0.002 per quiz
- Budget ~$5-10 for testing and evaluation

### Total Cost
- Can be done entirely free or under $10
