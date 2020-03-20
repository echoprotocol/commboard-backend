import os
import time
import argparse
from utils.db import get_influxdb_client, get_redis_client


def ping(client):
    try:
        return client.ping()
    except Exception:
        return None


def run(influxdb, redis, command):
    if ping(influxdb) and ping(redis):
        os.system(command)
    else:
        time.sleep(1)
        run(influxdb, redis, command)

if __name__ == '__main__':
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
