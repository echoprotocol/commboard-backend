import requests
from config import COINMARKETCAP_API_URL, COINMARKETCAP_API_KEY


def get_rate(currency='BTC,ETH', convert='USD'):
    parameters = {
        'symbol': currency,
        'convert': convert
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY,
    }
    try:
        response = requests.get(
            '{}{}'.format(
                COINMARKETCAP_API_URL,
                'cryptocurrency/quotes/latest'
            ),
            params=parameters,
            headers=headers
        )
        data = response.json()
        return data['data']
    except:
        return None


def get_public_ip():
    return requests.get("https://api.ipify.org").text
