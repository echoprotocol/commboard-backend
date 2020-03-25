from datetime import datetime
from psutil import cpu_percent, virtual_memory, disk_usage
from utils import get_redis_client, get_influxdb_client
from app import celery


@celery.task()
def update_pc_information():
    cpu, ram, free_space = cpu_percent(), virtual_memory()[2], disk_usage('.').free * 1e-9
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

    redis_client = get_redis_client()
    redis_client.set(
        'free_space',
        free_space,
        ex=90
    )

    influxdb_client = get_influxdb_client()
    influxdb_client.write_points(influxdb_points)
