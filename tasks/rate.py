from utils.db import get_redis_client
from utils.coinmarketcap import get_rate
from app import celery


@celery.task()
def update_currencies_rate():
    currencies_rate = get_rate()
    redis_client = get_redis_client()
    redis_client.set(
        'BTC',
        str(currencies_rate['BTC']['quote']['USD']['price'])
    )
    redis_client.set(
        'ETH',
        str(currencies_rate['BTC']['quote']['USD']['price'])
    )
