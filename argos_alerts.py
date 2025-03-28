import requests
import json

def send_telegram_alert(message, token, chat_id):
    """
    Sends a formatted alert to a Telegram chat.
    """
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(f"❌ Telegram alert failed: {response.status_code} – {response.text}")
    except Exception as e:
        print(f"🚨 Error sending Telegram alert: {e}")
