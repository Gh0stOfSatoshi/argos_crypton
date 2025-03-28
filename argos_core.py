# argos_core.py

import requests
import time
from datetime import datetime, timezone

def fetch_coin_data(coin):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}"
    params = {
        'localization': 'false',
        'tickers': 'false',
        'market_data': 'true',
        'community_data': 'false',
        'developer_data': 'false',
        'sparkline': 'false'
    }

    attempt = 0
    max_attempts = 5
    backoff = 1

    while attempt < max_attempts:
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                market = data.get('market_data', {})
                return {
                    'price': market.get('current_price', {}).get('usd'),
                    'volume': market.get('total_volume', {}).get('usd'),
                    'change_24h': market.get('price_change_percentage_24h')
                }
            elif response.status_code == 429:
                print(f"⚠️ Rate limited while fetching {coin}. Sleeping {backoff}s...")
                time.sleep(backoff)
                backoff *= 2
            else:
                print(f"❌ Failed to fetch {coin}: {response.status_code}")
                break
        except Exception as e:
            print(f"💥 Error on attempt {attempt+1} for {coin}: {e}")
            time.sleep(backoff)
            backoff *= 2
        attempt += 1

    return None

def get_utc_timestamp():
    return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
