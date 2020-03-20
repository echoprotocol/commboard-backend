import requests
from config import COINMARKETCAP_API_URL, COINMARKETCAP_API_KEY

def get_rate(currency='BTC,ETH', convert='USD'):
    url = 'cryptocurrency/quotes/latest'
    parameters = {
        'symbol': currency,
        'convert': convert
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY,
    }
    try:
        response = requests.get("{}{}".format(COINMARKETCAP_API_URL, url), params=parameters, headers=headers)
        data = response.json()
        return data['data']
    except:
        return None
