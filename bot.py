import os
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_crypto_data():
    """Stáhne data pro BTC, ETH a SOL včetně 24h změny"""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true"
        response = requests.get(url, timeout=10)
        return response.json()
    except Exception as e:
        print(f"Chyba při stahování dat: {e}")
        return None

def send_telegram_message(message):
    """Pošle zprávu formátovanou přes HTML do Telegramu"""
    if not TELEGRAM_TOKEN or not CHAT_ID:
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML" # Použijeme HTML tagy pro pokročilý styling
    }
    
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Message sending fail {e}")

def main():
    print("Generating a crypto report")
    data = get_crypto_data()
    
    if data:
        btc_price = data["bitcoin"]["usd"]
        btc_change = data["bitcoin"]["usd_24h_change"]
        
        eth_price = data["ethereum"]["usd"]
        eth_change = data["ethereum"]["usd_24h_change"]
        
        sol_price = data["solana"]["usd"]
        sol_change = data["solana"]["usd_24h_change"]

        def format_change(change):
            emoji = "🟢" if change >= 0 else "🔴"
            sign = "+" if change >= 0 else ""
            return f"{emoji} <code>{sign}{change:.2f}%</code>"

        # Skládání zprávy pomocí HTML tagů (<b> tučné, <code> monospace rámeček)
        message = (
            "💎 <b>CRYPTO MARKET PULSE</b> 💎\n"
            "<code>━━━━━━━━━━━━━━━━━━━━━━━</code>\n\n"
            "<b>🪙 Bitcoin (BTC)</b>\n"
            f"• Cena: <code>${btc_price:,.2f} USD</code>\n"
            f"• 24h: {format_change(btc_change)}\n\n"
            "<b>🔷 Ethereum (ETH)</b>\n"
            f"• Cena: <code>${eth_price:,.2f} USD</code>\n"
            f"• 24h: {format_change(eth_change)}\n\n"
            "<b>⚡ Solana (SOL)</b>\n"
            f"• Cena: <code>${sol_price:,.2f} USD</code>\n"
            f"• 24h: {format_change(sol_change)}\n\n"
            "<code>━━━━━━━━━━━━━━━━━━━━━━━</code>\n"
            "<i>🤖 Updated message every 15 minutes</i>"
        )
        
        send_telegram_message(message)
        print("Report sent succesfully")
    else:
        print("Failed to get API acess.")

if __name__ == "__main__":
    main()
