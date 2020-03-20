from datetime import datetime
from psutil import cpu_percent, virtual_memory, disk_usage
from utils.db import get_redis_client, get_influxdb_client
from app import celery


@celery.task()
def update_pc_information():
    cpu, ram, free_space = cpu_percent(), virtual_memory()[2], disk_usage('.').free * 1e-9

    redis_client = get_redis_client()
    redis_client.set(
        'free_space',
        str(free_space)
    )

    influxdb_client = get_influxdb_client()
    time = str(datetime.utcnow())
    influxdb_points = [
        {
            'measurement': 'cpu',
            'time': time,
            'fields': {
                'value': cpu
            }
        },
        {
            'measurement': 'ram',
            'time': time,
            'fields': {
                'value': ram
            }
        }
    ]

    influxdb_client.write_points(influxdb_points)
