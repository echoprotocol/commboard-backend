from utils import get_redis_client, get_rate
from app import celery


@celery.task()
def update_currencies_rate():
    currencies_rate = get_rate()
    redis_client = get_redis_client()
    for asset in ['BTC', 'ETH']:
        redis_client.set(
            asset.lower(),
            str(currencies_rate[asset]['quote']['USD']['price']),
            ex=90
        )
