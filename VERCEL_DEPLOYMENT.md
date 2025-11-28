# Vercel Deployment Guide for TDS Project 2

## Quick Deploy to Vercel

### Option 1: Deploy via Vercel CLI
1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   vercel
   ```

### Option 2: Deploy via GitHub (Recommended)
1. **Go to**: https://vercel.com/new
2. **Import your GitHub repository**: `23f3004345/tds-project-2`
3. **Set Environment Variable**:
   - Add `IITM_AI_TOKEN` with value: `eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIzZjMwMDQzNDVAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.Dt18UPV-D5WnpMRF_DQxnNTksLXPqxXs8qo6df2o7L4`
4. **Click Deploy**

### Your API will be available at:
```
https://tds-project-2.vercel.app
```

## Testing
```bash
python test_deployed_api.py https://tds-project-2.vercel.app
```

## Why Vercel?
- ✅ **No cold starts** for this use case
- ✅ **Free tier** with good limits
- ✅ **GitHub integration** - auto-deploy on push
- ✅ **Fast global CDN**
- ✅ **Reliable** - enterprise-grade infrastructure
- ✅ **Perfect for FastAPI** - excellent Python support

## Environment Variables Already Configured
All variables except the secret token are pre-configured in `vercel.json`. You only need to add `IITM_AI_TOKEN` in the Vercel dashboard.