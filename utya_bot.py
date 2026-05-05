import os
import asyncio
import logging
import json
from datetime import datetime
from telegram import Bot
from telegram.error import TelegramError
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHECK_INTERVAL = 300  # 5 minutes in seconds
BANNER_PATH = "utya_banner.jpg"

# UTYA token contract address on TON
UTYA_CONTRACT = "EQBaCgUwOoc6gHCNln_oJzb0mVs79YG7wYoavh-o1ItaneLA"

# Store user addresses and investments (in production, use a database)
user_addresses = {}
user_investments = {}  # Store initial investment amounts
market_cap_alerts = {}  # Store last alerted market cap milestone for each user

def get_utya_price():
    """Fetch UTYA price and calculate market cap"""
    try:
        # Try GeckoTerminal first
        url = f"https://api.geckoterminal.com/api/v2/networks/ton/tokens/{UTYA_CONTRACT}"
        headers = {'Accept': 'application/json'}
        
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            token_data = data.get('data', {}).get('attributes', {})
            price_usd = float(token_data.get('price_usd', 0))
            
            if price_usd > 0:
                # Market cap = price × 1 billion (total supply)
                market_cap = price_usd * 1_000_000_000
                logger.info(f"UTYA Price: ${price_usd:.8f}, Market Cap: ${market_cap:,.2f} (from GeckoTerminal)")
                return price_usd, market_cap
        
        # Fallback to STON.fi
        base_url = "https://api.ston.fi/v1"
        headers = {'Accept': 'application/json', 'User-Agent': 'Mozilla/5.0'}
        
        asset_url = f"{base_url}/assets/{UTYA_CONTRACT}"
        response = requests.get(asset_url, headers=headers, timeout=15)
        response.raise_for_status()
        asset_data = response.json()['asset']
        
        price_usd = float(asset_data.get('dex_price_usd', 0))
        
        # Market cap = price × 1 billion (total supply)
        market_cap = price_usd * 1_000_000_000
        
        logger.info(f"UTYA Price: ${price_usd:.8f}, Market Cap: ${market_cap:,.2f}")
        return price_usd, market_cap
        
    except Exception as e:
        logger.error(f"Error fetching UTYA price: {e}")
        return 0, 0

def get_utya_balance(address):
    """Get UTYA balance for a TON address using TonAPI"""
    try:
        # TonAPI endpoint for account jettons
        url = f"https://tonapi.io/v2/accounts/{address}/jettons"
        headers = {'Accept': 'application/json'}
        
        logger.info(f"Fetching jettons for address: {address[:8]}...")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        logger.info(f"Found {len(data.get('balances', []))} jettons for {address[:8]}...")
        
        # Find UTYA jetton in the list
        for jetton in data.get('balances', []):
            jetton_address = jetton.get('jetton', {}).get('address', '')
            jetton_symbol = jetton.get('jetton', {}).get('symbol', '')
            
            logger.info(f"Checking jetton: {jetton_symbol} ({jetton_address[:8]}...)")
            
            # Check if this is UTYA by address or symbol
            if (jetton_address.lower() == UTYA_CONTRACT.lower() or 
                jetton_symbol.upper() == 'UTYA'):
                # Get balance and decimals
                balance = int(jetton.get('balance', 0))
                decimals = int(jetton.get('jetton', {}).get('decimals', 9))
                utya_balance = balance / (10 ** decimals)
                logger.info(f"✅ Address {address[:8]}... has {utya_balance:,.2f} UTYA")
                return utya_balance
        
        logger.info(f"❌ No UTYA found for address {address[:8]}...")
        return 0
        
    except Exception as e:
        logger.error(f"Error fetching balance for {address}: {e}")
        if 'response' in locals():
            logger.error(f"Response: {response.text[:500]}")
        return 0

def format_number(num):
    """Format large numbers with K, M, B suffixes"""
    if num is None or num == 0:
        return "$0.00"
    
    if num >= 1_000_000_000:
        return f"${num/1_000_000_000:.2f}B"
    elif num >= 1_000_000:
        return f"${num/1_000_000:.2f}M"
    elif num >= 1_000:
        return f"${num/1_000:.2f}K"
    else:
        return f"${num:.2f}"

async def send_update(bot, chat_id):
    """Send UTYA balance update to user"""
    try:
        addresses = user_addresses.get(chat_id, [])
        if not addresses:
            return
        
        # Get UTYA price and market cap
        price, market_cap = get_utya_price()
        if price == 0:
            await bot.send_message(
                chat_id=chat_id,
                text="❌ Unable to fetch UTYA price. Will retry in 5 minutes.",
                parse_mode='HTML'
            )
            return
        
        # Check for market cap milestones (every $50M)
        current_milestone = int(market_cap / 50_000_000) * 50_000_000
        last_milestone = market_cap_alerts.get(chat_id, 0)
        
        milestone_alert = False
        if current_milestone > last_milestone and current_milestone >= 50_000_000:
            milestone_alert = True
            market_cap_alerts[chat_id] = current_milestone
        
        # Get total balance across all addresses
        total_balance = 0
        for address in addresses:
            balance = get_utya_balance(address)
            total_balance += balance
        
        # Calculate value
        total_value = total_balance * price
        
        # Create message
        message = f"""<b>💎 UTYA</b>

<b>Market Cap:</b> {format_number(market_cap)}
<b>Price:</b> ${price:.8f}

<b>Your Holdings:</b> {format_number(total_value)}
({total_balance:,.2f} UTYA)

<b>Addresses tracked:</b> {len(addresses)}"""
        
        # Add profit/loss for specific user (your chat ID)
        investment = user_investments.get(chat_id, 0)
        if investment > 0:
            profit = total_value - investment
            profit_percent = (profit / investment) * 100
            profit_emoji = "🟢" if profit >= 0 else "🔴"
            profit_sign = "+" if profit >= 0 else ""
            
            message += f"""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<b>💰 P&L</b>
<b>Investment:</b> ${investment:,.2f}
<b>Current Value:</b> {format_number(total_value)}
{profit_emoji} <b>Profit:</b> {profit_sign}${profit:,.2f} ({profit_sign}{profit_percent:.2f}%)"""
        
        # Add milestone alert if triggered
        if milestone_alert:
            message = f"""🚨 <b>MILESTONE ALERT!</b> 🚨
<b>Market Cap Hit: {format_number(current_milestone)}</b>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

""" + message
        
        # Send with banner
        if os.path.exists(BANNER_PATH):
            with open(BANNER_PATH, 'rb') as photo:
                await bot.send_photo(
                    chat_id=chat_id,
                    photo=photo,
                    caption=message,
                    parse_mode='HTML'
                )
        else:
            await bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode='HTML'
            )
        
        logger.info(f"Update sent to chat {chat_id}: {total_balance:,.2f} UTYA = {format_number(total_value)} | Market Cap: {format_number(market_cap)}")
        if milestone_alert:
            logger.info(f"🚨 MILESTONE ALERT for {chat_id}: {format_number(current_milestone)}")
        
    except Exception as e:
        logger.error(f"Error sending update to {chat_id}: {e}")

async def handle_message(bot, message):
    """Handle incoming messages"""
    chat_id = message.chat_id
    text = message.text.strip()
    
    # Check if it's /start command
    if text == '/start':
        welcome_message = """🦆 <b>Welcome to UTYA Tracker Bot!</b>

Send me your TON wallet address(es) to track your UTYA holdings.

<b>You can send:</b>
• One address: <code>EQAbc...</code>
• Multiple addresses (one per line):
<code>EQAbc...
EQDef...
EQGhi...</code>

I'll check your balance and send updates every 5 minutes! 💰

<b>Commands:</b>
/start - Start tracking
/stop - Stop tracking"""
        
        await bot.send_message(
            chat_id=chat_id,
            text=welcome_message,
            parse_mode='HTML'
        )
        return
    
    # Check if it's /stop command
    if text == '/stop':
        if chat_id in user_addresses:
            del user_addresses[chat_id]
            
            # Save to file
            try:
                with open('user_addresses.json', 'w') as f:
                    json.dump(user_addresses, f)
            except Exception as e:
                logger.error(f"Error saving addresses: {e}")
            
            await bot.send_message(
                chat_id=chat_id,
                text="✅ Stopped tracking your addresses. Send /start to begin again.",
                parse_mode='HTML'
            )
            logger.info(f"User {chat_id} stopped tracking")
        else:
            await bot.send_message(
                chat_id=chat_id,
                text="You're not currently being tracked. Send /start to begin!",
                parse_mode='HTML'
            )
        return
    
    # Parse addresses (one per line or comma separated)
    addresses = []
    for line in text.replace(',', '\n').split('\n'):
        addr = line.strip()
        if addr and (addr.startswith('EQ') or addr.startswith('UQ')):
            addresses.append(addr)
    
    if not addresses:
        await bot.send_message(
            chat_id=chat_id,
            text="❌ No valid TON addresses found. Please send addresses starting with EQ or UQ.",
            parse_mode='HTML'
        )
        return
    
    # Store addresses for this user
    user_addresses[chat_id] = addresses
    
    # Save to file (simple persistence)
    try:
        with open('user_addresses.json', 'w') as f:
            json.dump(user_addresses, f)
    except Exception as e:
        logger.error(f"Error saving addresses: {e}")
    
    await bot.send_message(
        chat_id=chat_id,
        text=f"✅ Saved {len(addresses)} address(es)!\n\nFetching your balance...",
        parse_mode='HTML'
    )
    
    # Send first update immediately
    await send_update(bot, chat_id)

async def main():
    """Main bot loop"""
    if not BOT_TOKEN:
        logger.error("Bot token not found! Please set TELEGRAM_BOT_TOKEN in .env file")
        return
    
    # Load saved addresses
    try:
        if os.path.exists('user_addresses.json'):
            with open('user_addresses.json', 'r') as f:
                loaded = json.load(f)
                # Convert string keys back to int
                for k, v in loaded.items():
                    user_addresses[int(k)] = v
            logger.info(f"Loaded {len(user_addresses)} users from file")
    except Exception as e:
        logger.error(f"Error loading addresses: {e}")
    
    # Load saved investments
    try:
        if os.path.exists('user_investments.json'):
            with open('user_investments.json', 'r') as f:
                loaded = json.load(f)
                # Convert string keys back to int
                for k, v in loaded.items():
                    user_investments[int(k)] = float(v)
            logger.info(f"Loaded investments for {len(user_investments)} users")
    except Exception as e:
        logger.error(f"Error loading investments: {e}")
    
    # Set your investment amount (your chat ID)
    # You can find your chat ID from the logs when you message the bot
    YOUR_CHAT_ID = 8251311862  # Replace with your actual chat ID if different
    user_investments[YOUR_CHAT_ID] = 648.0  # Updated: $560 + $88
    
    # Initialize market cap alerts at current level
    market_cap_alerts[YOUR_CHAT_ID] = 0  # Will trigger first alert at next $50M milestone
    
    # Save investments
    try:
        with open('user_investments.json', 'w') as f:
            json.dump(user_investments, f)
    except Exception as e:
        logger.error(f"Error saving investments: {e}")
    
    bot = Bot(token=BOT_TOKEN)
    
    # Get bot info
    try:
        bot_info = await bot.get_me()
        logger.info(f"Bot started: @{bot_info.username}")
        print(f"\n✅ UTYA Tracker Bot is running: @{bot_info.username}")
        print(f"📱 Users can send /start to begin tracking")
        print(f"⏰ Updates will be sent every 5 minutes")
        print(f"💾 Tracking {len(user_addresses)} users\n")
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        return
    
    last_update_id = 0
    
    # Main loop
    while True:
        try:
            # Get updates
            updates = await bot.get_updates(offset=last_update_id + 1, timeout=10)
            
            for update in updates:
                last_update_id = update.update_id
                
                if update.message and update.message.text:
                    await handle_message(bot, update.message)
            
            # Check if it's time to send periodic updates
            current_time = datetime.now()
            if not hasattr(main, 'last_periodic_update'):
                main.last_periodic_update = current_time
            
            time_since_last = (current_time - main.last_periodic_update).total_seconds()
            
            if time_since_last >= CHECK_INTERVAL:
                logger.info("Sending periodic updates...")
                for chat_id in list(user_addresses.keys()):
                    try:
                        await send_update(bot, chat_id)
                    except Exception as e:
                        logger.error(f"Error in periodic update for {chat_id}: {e}")
                
                main.last_periodic_update = current_time
            
            await asyncio.sleep(1)
            
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
            break
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
