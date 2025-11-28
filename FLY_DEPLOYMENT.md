# Fly.io Deployment Guide for TDS Project 2

## Prerequisites
1. Install flyctl CLI: https://fly.io/docs/hands-on/install-flyctl/
2. Sign up for Fly.io account (free tier available)

## Quick Deploy Steps

1. **Install flyctl**:
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   ```

2. **Login to Fly.io**:
   ```bash
   fly auth login
   ```

3. **Deploy the application**:
   ```bash
   fly launch --no-deploy
   fly deploy
   ```

4. **Your app will be available at**:
   ```
   https://tds-project-2.fly.dev
   ```

## Environment Variables
All required environment variables are already configured in `fly.toml`:
- LLM_PROVIDER=iitm
- IITM_API_BASE_URL=https://llm.iitm.ac.in/v1
- EMAIL=23f3004345@ds.study.iitm.ac.in
- SECRET=my-secure-secret-123

## Important Notes
- ✅ **No sleep issues** - Fly.io keeps apps running
- ✅ **Free tier available** - Good for evaluation
- ✅ **Fast deployment** - Usually deploys in 2-3 minutes
- ✅ **Reliable** - Better uptime than Render/Railway free tiers

## Set Secret Token
After deployment, set your IITM AI token:
```bash
fly secrets set IITM_AI_TOKEN="eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIzZjMwMDQzNDVAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.Dt18UPV-D5WnpMRF_DQxnNTksLXPqxXs8qo6df2o7L4"
```

## Testing
Test your deployment:
```bash
python test_deployed_api.py https://tds-project-2.fly.dev
```