# UTYA Tracker Bot - Railway Deployment Guide

## 🚀 Quick Deploy to Railway

### Step 1: Prepare Your Files
1. Make sure you have all these files:
   - `utya_bot.py`
   - `requirements.txt`
   - `.env`
   - `Procfile`
   - `runtime.txt`
   - `railway.json`
   - `utya_banner.jpg` (your banner image)

### Step 2: Create Railway Project
1. Go to [railway.app](https://railway.app)
2. Sign up/Login with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo" OR "Empty Project"

### Step 3: Upload Files (if using Empty Project)
1. Click "New" → "Empty Service"
2. Go to "Settings" tab
3. Under "Source" click "Connect Repo" or use Railway CLI

### Step 4: Set Environment Variables
In Railway dashboard, go to "Variables" tab and add:

```
TELEGRAM_BOT_TOKEN=8610282554:AAG22ygwTk3_3U1N7900m22X9rT1ubQSj_c
UTYA_AMOUNT=15450
```

### Step 5: Deploy
1. Railway will automatically detect Python and install dependencies
2. It will run `python utya_bot.py` automatically
3. Check "Deployments" tab for logs

### Step 6: Verify It's Running
1. Go to "Deployments" → Click latest deployment
2. Check logs - you should see "Bot is running"
3. Send `/start` to your bot on Telegram

## 📝 Important Notes

- **Banner Image**: Make sure `utya_banner.jpg` is uploaded
- **Persistence**: User data is stored in JSON files (will reset on redeploy)
- **Logs**: Check Railway logs if bot isn't responding
- **Cost**: Railway free tier should be enough for this bot

## 🔧 Troubleshooting

**Bot not responding?**
- Check Railway logs for errors
- Verify TELEGRAM_BOT_TOKEN is correct
- Make sure deployment is "Active"

**Market cap showing $0?**
- API might be rate limited
- Check logs for API errors
- Wait a few minutes and try again

**No banner image?**
- Upload `utya_banner.jpg` to your repo
- Check file path in logs

## 🎯 Your Bot Features

✅ Tracks UTYA balance from TON addresses
✅ Updates every 5 minutes
✅ Market cap alerts every $50M
✅ P&L tracking (investment: $648)
✅ Beautiful banner with each update

## 📊 Commands

- `/start` - Start tracking (send your TON address)
- `/stop` - Stop tracking

Your bot will automatically send updates every 5 minutes! 🦆🚀
