# Deployment with ngrok (No Sleep Issues!)

## Why ngrok for Evaluation?

✅ **No sleep/spin-down issues** - Your local machine controls uptime
✅ **Instant startup** - No cold start delays
✅ **Free tier sufficient** - Works perfectly for 1-hour evaluation
✅ **You control everything** - Can monitor and restart instantly

## Setup (5 minutes)

### 1. Download ngrok
```powershell
# Visit: https://ngrok.com/download
# Or use: winget install ngrok
```

### 2. Sign up (Free)
- Go to: https://dashboard.ngrok.com/signup
- Get your authtoken

### 3. Configure ngrok
```powershell
ngrok config add-authtoken YOUR_AUTH_TOKEN
```

### 4. Start your server
```powershell
# Terminal 1
python main.py
```

### 5. Start ngrok tunnel
```powershell
# Terminal 2
ngrok http 8000
```

You'll get a URL like: `https://abc123.ngrok-free.app`

## ⚠️ Important for Evaluation Day (Nov 29)

### Morning Setup (2:30 PM IST)
1. Start `python main.py`
2. Start `ngrok http 8000`
3. Copy the HTTPS URL
4. **Keep both terminals running**
5. Don't close your laptop/computer

### During Evaluation (3:00-4:00 PM IST)
- ✅ Server stays running (no sleep!)
- ✅ Instant response (no cold start)
- ✅ You can see logs in real-time
- ✅ Can restart if needed

### After Evaluation
- Stop ngrok (Ctrl+C)
- Stop server (Ctrl+C)

## 🎯 ngrok Pro Tips

**Free tier limits:**
- 1 online ngrok process
- 40 connections/minute (enough for evaluation)
- Random URL each time (but stable during session)

**URL stays same** as long as ngrok is running!

## 💡 Best Strategy

### For Google Form Submission
If submitting early (before Nov 29):
- Use a Railway/cloud URL (if it works)
- OR submit on Nov 29 morning with ngrok URL

### On Evaluation Day (Nov 29)
1. **2:30 PM:** Start server + ngrok
2. **2:45 PM:** Update Google Form with ngrok URL (if needed)
3. **3:00-4:00 PM:** Keep computer ON and running
4. **4:00 PM:** Evaluation ends, you can stop

## 📝 ngrok URL Example
```
https://1234-56-78-90-12.ngrok-free.app/quiz
```

This is your API endpoint URL for the form!
