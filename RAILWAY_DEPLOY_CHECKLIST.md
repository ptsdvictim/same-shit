# 🚀 Railway Deployment Checklist

## ✅ Pre-Deployment Verification

### Files Ready for Upload:
- [x] `utya_bot.py` - Main bot code
- [x] `requirements.txt` - Python dependencies
- [x] `Procfile` - Railway process configuration
- [x] `runtime.txt` - Python version specification
- [x] `railway.json` - Railway deployment settings
- [x] `utya_banner.jpg` - Banner image (IMPORTANT: Must be included!)
- [x] `.gitignore` - Configured to exclude sensitive files but INCLUDE banner
- [x] `README_RAILWAY.md` - Deployment instructions

### Files to EXCLUDE (already in .gitignore):
- `.env` - Contains sensitive token (set in Railway dashboard instead)
- `user_addresses.json` - User data (will be created on Railway)
- `user_investments.json` - Investment data (will be created on Railway)
- `utya_files/` - Unnecessary downloaded files
- `xd.jpg` - Not needed

## 📋 Deployment Steps

### 1. Upload to Railway
**Option A: GitHub (Recommended)**
1. Create a new GitHub repository
2. Push all files to GitHub (excluding .gitignore files)
3. Connect Railway to your GitHub repo

**Option B: Railway CLI**
```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

**Option C: Manual Upload**
1. Create ZIP file with these files:
   - utya_bot.py
   - requirements.txt
   - Procfile
   - runtime.txt
   - railway.json
   - utya_banner.jpg
2. Upload to Railway

### 2. Configure Environment Variables in Railway Dashboard
Go to your Railway project → Variables tab → Add:

```
TELEGRAM_BOT_TOKEN=8610282554:AAG22ygwTk3_3U1N7900m22X9rT1ubQSj_c
```

**Note:** `UTYA_AMOUNT` is not needed - it's hardcoded in the bot for your chat ID (8251311862)

### 3. Deploy & Monitor
1. Railway will auto-detect Python and install dependencies
2. Check "Deployments" tab for build logs
3. Look for: "✅ UTYA Tracker Bot is running"
4. Verify no errors in logs

### 4. Test Your Bot
1. Open Telegram
2. Find your bot: @your_bot_username
3. Send `/start`
4. Send your TON address(es)
5. Wait for first update (should be immediate)
6. Verify updates come every 5 minutes

## 🔍 Verification Checklist

After deployment, verify:
- [ ] Bot responds to `/start` command
- [ ] Bot accepts TON addresses (EQ... or UQ...)
- [ ] Banner image appears in updates
- [ ] Market cap displays correctly
- [ ] Your holdings value is calculated
- [ ] P&L section shows (for your chat ID: 8251311862)
- [ ] Updates arrive every 5 minutes
- [ ] `/stop` command works

## 🐛 Troubleshooting

### Bot not responding?
```bash
# Check Railway logs
1. Go to Deployments tab
2. Click latest deployment
3. Check for errors
```

Common issues:
- **"Bot token invalid"** → Check TELEGRAM_BOT_TOKEN in Variables
- **"Module not found"** → Check requirements.txt is uploaded
- **"No banner image"** → Verify utya_banner.jpg is uploaded
- **"Market cap $0"** → API rate limit, wait a few minutes

### Market Cap Issues
- Price API might be temporarily down
- Bot will retry every 5 minutes
- Check logs for API error messages

### Missing Banner
- Verify `utya_banner.jpg` is in root directory
- Check Railway file browser to confirm upload
- Look for "Banner not found" in logs

## 📊 Your Bot Configuration

**Investment Tracking:**
- Your Chat ID: `8251311862`
- Total Investment: `$648` ($560 initial + $88 TON swap)
- UTYA Amount: `15,450` tokens

**Features Enabled:**
- ✅ Multi-address tracking
- ✅ 5-minute updates
- ✅ Market cap alerts (every $50M)
- ✅ P&L tracking (for your chat ID only)
- ✅ Banner image with each update

**API Sources:**
- Primary: GeckoTerminal API
- Fallback: STON.fi API
- Balance: TonAPI (tonapi.io)

## 🎯 Expected Behavior

**First Message:**
- Welcome message with instructions
- Prompts for TON address

**After Address Submission:**
- Confirmation message
- Immediate first update with banner
- Shows market cap, price, holdings, P&L

**Every 5 Minutes:**
- Automatic update with current data
- Banner image included
- P&L section (for you only)

**Milestone Alerts:**
- 🚨 Alert when market cap crosses $50M, $100M, $150M, etc.
- Only triggers once per milestone
- Includes all regular update info

## 💡 Tips

1. **Keep Railway logs open** during first deployment
2. **Test immediately** after deployment
3. **Monitor for 15 minutes** to ensure updates work
4. **Check milestone alerts** by watching market cap changes
5. **Backup user data** periodically (download JSON files from Railway)

## 🔐 Security Notes

- Bot token is stored in Railway environment variables (secure)
- `.env` file is excluded from deployment
- User data stored in JSON files on Railway filesystem
- No sensitive data in code repository

## 📞 Support

If issues persist:
1. Check Railway community forums
2. Review Railway Python deployment docs
3. Verify all environment variables are set
4. Ensure Python 3.11 is specified in runtime.txt

---

**Ready to deploy!** 🚀

All files are configured and ready for Railway upload.
