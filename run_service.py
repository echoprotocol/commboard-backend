import os
import time
import argparse
from utils import get_influxdb_client, get_redis_client, get_echo_client, get_echo_head_block_num


def ping(client):
    try:
        return client.ping()
    except Exception:
        return None


def ping_echo():
    try:
        echo_client = get_echo_client()
        return get_echo_head_block_num(echo_client)
    except Exception:
        return None


def run(influxdb, redis, command):
    if ping(influxdb) and ping(redis) and ping_echo():
        os.system(command)
    else:
        time.sleep(1)
        run(influxdb, redis, command)


parser = argparse.ArgumentParser()
parser.add_argument('service', type=str, choices=['web', 'celery'], help='Select service to run')
args = parser.parse_args()

run(
    get_influxdb_client(),
    get_redis_client(),
    'flask run --host=0.0.0.0 --port=5000' if args.service == 'web' else 'celery -A app.celery worker -l debug -B'
)
