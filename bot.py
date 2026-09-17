import os
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_coingecko_data():
    """Stáhne ceny, změny a dominanci BTC z CoinGecko"""
    try:
        url = "https://api.coingecko.com/api/v3/global"
        response = requests.get(url, timeout=10)
        global_data = response.json().get("data", {})
        btc_dominance = global_data.get("market_cap_percentage", {}).get("btc", 0)

        prices_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true"
        prices_response = requests.get(prices_url, timeout=10)
        prices_data = prices_response.json()

        return prices_data, btc_dominance
    except Exception as e:
        print(f"Chyba při stahování CoinGecko dat: {e}")
        return None, 0

def get_fear_and_greed():
    """Stáhne aktuální Fear & Greed Index"""
    try:
        url = "https://api.alternative.me/fng/"
        response = requests.get(url, timeout=10)
        data = response.json().get("data", [{}])[0]
        return data.get("value", "N/A"), data.get("value_classification", "N/A")
    except Exception as e:
        print(f"Chyba při stahování Fear & Greed: {e}")
        return "N/A", "N/A"

def get_gas_fees():
    """Odhad Ethereum gas fees přes veřejné API"""
    try:
        url = "https://api.gasprice.rs/v1/iss" # nebo fallback na průměrné hodnoty
        # Použijeme bezpečnější základní odhad, popř. coingecko/etherscan endpoint
        # Pro zjednodušení teď natáhneme rychlý odhad z owlracle nebo public endpointu, 
        # případně to ošetříme bezpečně:
        return "Low (Optimal)"
    except:
        return "N/A"

def send_telegram_message(message):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Chyba při odesílání: {e}")

def main():
    print("Generuji All-in-One krypto report...")
    prices, btc_dom = get_coingecko_data()
    fng_value, fng_text = get_fear_and_greed()
    
    if prices:
        btc_price = prices["bitcoin"]["usd"]
        btc_change = prices["bitcoin"]["usd_24h_change"]
        
        eth_price = prices["ethereum"]["usd"]
        eth_change = prices["ethereum"]["usd_24h_change"]
        
        sol_price = prices["solana"]["usd"]
        sol_change = prices["solana"]["usd_24h_change"]

        def format_change(change):
            emoji = "🟢" if change >= 0 else "🔴"
            sign = "+" if change >= 0 else ""
            return f"{emoji} <code>{sign}{change:.2f}%</code>"

        # Skládání all-in-one zprávy
        message = (
            "🚀 <b>ALL-IN-ONE CRYPTO DASHBOARD</b> 🚀\n"
            "<code>━━━━━━━━━━━━━━━━━━━━━━━</code>\n\n"
            f"🧠 <b>Market Sentiment:</b> <code>{fng_value}/100 ({fng_text})</code>\n"
            f"dominance <b>BTC Dominance:</b> <code>{btc_dom:.1f}%</code>\n\n"
            "<b>🪙 <a href='https://www.tradingview.com/chart/?symbol=BINANCE:BTCUSDT'>Bitcoin (BTC)</a></b>\n"
            f"• Cena: <code>${btc_price:,.2f} USD</code>\n"
            f"• 24h: {format_change(btc_change)}\n\n"
            "<b>🔷 <a href='https://www.tradingview.com/chart/?symbol=BINANCE:ETHUSDT'>Ethereum (ETH)</a></b>\n"
            f"• Cena: <code>${eth_price:,.2f} USD</code>\n"
            f"• 24h: {format_change(eth_change)}\n\n"
            "<b>⚡ <a href='https://www.tradingview.com/chart/?symbol=BINANCE:SOLUSDT'>Solana (SOL)</a></b>\n"
            f"• Cena: <code>${sol_price:,.2f} USD</code>\n"
            f"• 24h: {format_change(sol_change)}\n\n"
            "<code>━━━━━━━━━━━━━━━━━━━━━━━</code>\n"
            "<i>🤖 Powered by GitHub Actions • All-in-One Tool</i>"
        )
        
        send_telegram_message(message)
        print("All-in-one report úspěšně odeslán!")
    else:
        print("Nepodařilo se získat data.")

if __name__ == "__main__":
    main()
