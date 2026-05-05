# 🦆 UTYA Tracker Bot

A Telegram bot that tracks UTYA token price and your holdings on the TON blockchain.

## ✨ Features

- 🦆 **Real-time UTYA price tracking** - Live price from GeckoTerminal/STON.fi
- 💰 **Multi-address wallet tracking** - Track multiple TON wallets
- 📊 **Market cap monitoring** - Live market cap calculation
- 🚨 **Milestone alerts** - Alerts every $50M market cap milestone
- 💎 **Profit/Loss tracking** - Personal P&L for your investment
- 🖼️ **Beautiful banner** - UTYA banner with every update
- ⏰ **Automatic updates** - Updates every 5 minutes

## 🚀 Quick Start

### Local Development

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Create `.env` file:**
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

3. **Run the bot:**
```bash
python utya_bot.py
```

### Deploy to Railway (Recommended)

**See `DEPLOY_NOW.md` for quick deployment guide!**

Or read `README_RAILWAY.md` for detailed instructions.

## 📱 Bot Commands

- `/start` - Start tracking (bot will ask for your TON address)
- `/stop` - Stop tracking your addresses

## 🎯 How It Works

1. User sends `/start` command
2. User sends their TON wallet address(es) (EQ... or UQ...)
3. Bot fetches UTYA balance from TonAPI
4. Bot gets current price from GeckoTerminal/STON.fi
5. Bot calculates market cap (price × 1B supply)
6. Sends update with banner image
7. Repeats every 5 minutes automatically
8. Sends 🚨 alerts when market cap crosses $50M milestones

## 💰 Investment Tracking

For specific users (configurable in code), the bot shows:
- Initial investment amount
- Current value
- Profit/Loss with percentage
- Color-coded (🟢 profit / 🔴 loss)

## 🔧 Tech Stack

- **Python 3.11** - Runtime
- **python-telegram-bot 20.7** - Telegram Bot API
- **TonAPI** - TON blockchain balance queries
- **GeckoTerminal API** - Primary price source
- **STON.fi API** - Fallback price source
- **Railway** - Deployment platform (recommended)

## 📊 UTYA Token Info

- **Contract**: `EQBaCgUwOoc6gHCNln_oJzb0mVs79YG7wYoavh-o1ItaneLA`
- **Total Supply**: 1,000,000,000 UTYA
- **Network**: TON (The Open Network)
- **Decimals**: 9

## 📁 Project Structure

```
.
├── utya_bot.py                    # Main bot code
├── requirements.txt               # Python dependencies
├── Procfile                       # Railway process config
├── runtime.txt                    # Python version
├── railway.json                   # Railway deployment settings
├── utya_banner.jpg                # Banner image (104 KB)
├── .env                           # Environment variables (local)
├── .gitignore                     # Git ignore rules
├── README.md                      # This file
├── README_RAILWAY.md              # Railway deployment guide
├── RAILWAY_DEPLOY_CHECKLIST.md   # Detailed deployment checklist
├── DEPLOY_NOW.md                  # Quick deploy guide
├── user_addresses.json            # User wallet addresses (auto-created)
└── user_investments.json          # Investment tracking (auto-created)
```

## 🎨 Update Message Format

```
💎 UTYA

Market Cap: $42.18M
Price: $0.04218401

Your Holdings: $650.45
(15,450.00 UTYA)

Addresses tracked: 1

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 P&L
Investment: $648.00
Current Value: $650.45
🟢 Profit: +$2.45 (+0.38%)
```

## 🚨 Milestone Alerts

When market cap crosses $50M, $100M, $150M, etc.:

```
🚨 MILESTONE ALERT! 🚨
Market Cap Hit: $50.00M

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💎 UTYA
[... regular update ...]
```

## 🔐 Security

- Bot token stored in environment variables
- `.env` file excluded from git
- User data stored in local JSON files
- No sensitive data in code repository

## 📝 Configuration

Edit `utya_bot.py` to customize:

```python
CHECK_INTERVAL = 300  # Update interval (seconds)
YOUR_CHAT_ID = 8251311862  # Your Telegram chat ID
user_investments[YOUR_CHAT_ID] = 648.0  # Your investment
```

## 🐛 Troubleshooting

**Bot not responding?**
- Check bot token is correct
- Verify bot is running (check logs)
- Ensure you've sent `/start` first

**Market cap showing $0?**
- API might be rate limited
- Wait for next update (5 minutes)
- Check logs for API errors

**No banner image?**
- Verify `utya_banner.jpg` exists
- Check file path in code
- Ensure file is uploaded to Railway

## 📞 Support

- Check `RAILWAY_DEPLOY_CHECKLIST.md` for detailed troubleshooting
- Review Railway logs for errors
- Verify environment variables are set

## 🎉 Ready to Deploy?

**Read `DEPLOY_NOW.md` for the quickest path to deployment!**

All files are configured and ready for Railway upload. 🚀

---

Made with 💎 for UTYA holders 🦆
