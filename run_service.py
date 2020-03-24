import os
import time
import argparse
from utils.db import get_influxdb_client, get_redis_client
from utils.echo import get_echo_client


def ping(client):
    try:
        return client.ping()
    except Exception:
        return None


def get_echo_head_block_num():
    try:
        echo = get_echo_client()
        return echo.api.database.get_dynamic_global_properties()["head_block_number"]
    except Exception:
        return None


def run(influxdb, redis, command):
    if ping(influxdb) and ping(redis) and get_echo_head_block_num():
        os.system(command)
    else:
        time.sleep(1)
        run(influxdb, redis, command)


parser = argparse.ArgumentParser()
parser.add_argument('service', type=str, choices=['web', 'celery'], help='Select service to run')
args = parser.parse_args()

influxdb_client = get_influxdb_client()
redis_client = get_redis_client()

command = 'flask run' if args.service == 'web' else 'celery -A app.celery worker -l debug -B'
run(
    influxdb_client,
    redis_client,
    command
)
