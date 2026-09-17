import os
import requests

# Načtení tokenu z proměnných prostředí (bezpečně)
TELEGRAM_TOKEN = os.getenv("8881136619:AAG7JPMIL6ZG1g1Gtko9sH0GP00hcf-icqk")
# Příklad použití ID chatu, kam má zpráva dorazit (také může být v env proměnných)
CHAT_ID = os.getenv("7260268357")

def get_crypto_price():
    """Získá aktuální cenu BTC z veřejného CoinGecko API"""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        response = requests.get(url, timeout=10)
        data = response.json()
        price = data["bitcoin"]["usd"]
        return price
    except Exception as e:
        print(f"Chyba při stahování dat: {e}")
        return None

def send_telegram_message(message):
    """Pošle zprávu přes Telegrambota"""
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("Chybí Telegram token nebo Chat ID v proměnných prostředí!")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Chyba při odesílání zprávy na Telegram: {e}")

def main():
    print("Spouštím kontrolu krypto trhu...")
    price = get_crypto_price()
    
    if price:
        message = f"Aktuální cena Bitcoinu je: ${price} USD"
        print(message)
        send_telegram_message(message)
    else:
        print("Nepodařilo se získat cenu.")

if __name__ == "__main__":
    main()
