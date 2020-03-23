import os
import time
import argparse
from echopy import Echo
from utils.db import get_influxdb_client, get_redis_client
from config import ECHO_URL


def ping(client):
    try:
        return client.ping()
    except Exception:
        return None


def get_head_block_num(echo):
    try:
        echo.connect(ECHO_URL)
        return echo.api.database.get_dynamic_global_properties()["head_block_number"]
    except Exception:
        return None


def run(echo, influxdb, redis, command):
    if ping(influxdb) and ping(redis) and get_head_block_num(echo):
        os.system(command)
    else:
        time.sleep(1)
        run(echo, influxdb, redis, command)


parser = argparse.ArgumentParser()
parser.add_argument('service', type=str, choices=['web', 'celery'], help='Select service to run')
args = parser.parse_args()

influxdb_client = get_influxdb_client()
redis_client = get_redis_client()
echo = Echo()

command = 'flask run' if args.service == 'web' else 'celery -A app.celery worker -l debug -B'
run(
    echo,
    influxdb_client,
    redis_client,
    command
)
