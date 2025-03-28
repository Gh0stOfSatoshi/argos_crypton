# argos_daemon.py

import time
import json
from argos_core import fetch_coin_data
from argos_utils import get_utc_timestamp, log_debug
from argos_alerts import send_telegram_alert  # ✅ Alert function added

# Load config
with open("argos_config.json") as f:
    config = json.load(f)

coins = config.get("coins", [])
interval = config.get("interval_seconds", 60)
token = config.get("telegram_bot_token")
chat_id = config.get("telegram_chat_id")

def run_daemon():
    log_debug("✅ Daemon started.")

    while True:
        timestamp = get_utc_timestamp()
        print(f"\n🧠 Argos-Crypton Tick | {timestamp} UTC")

        for coin in coins:
            print(f"Querying: {coin}")
            data = fetch_coin_data(coin)

            if data:
                print(
                    f"{coin.upper()}: ${data['price']:,} | "
                    f"Vol: {data['volume']:,} | "
                    f"Δ24h: {data['change_24h']:+.2f}%"
                )

                # ✅ Send alert to Telegram
                message = (
                    f"{coin.upper()} Update:\n"
                    f"Price: ${data['price']:,}\n"
                    f"24h Change: {data['change_24h']:+.2f}%\n"
                    f"Volume: {data['volume']:,}"
                )
                send_telegram_alert(message, token, chat_id)

            else:
                print(f"{coin.upper()}: ❌ No data")

        log_debug("✅ Tick completed. Sleeping...\n")
        time.sleep(interval)

# Local test entry point
if __name__ == "__main__":
    run_daemon()


