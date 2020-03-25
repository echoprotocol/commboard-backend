from utils import get_redis_client, get_influxdb_client, get_echo_node_uptime,\
    get_echo_head_block_num, inspect_block_for_committee_operations
from app import celery


@celery.task()
def update_node_information():
    node_uptime = get_echo_node_uptime()
    redis_client = get_redis_client()
    redis_client.set(
        'uptime',
        node_uptime
    )

    echo_head_block_num = get_echo_head_block_num()
    inspection_head_block_num = redis_client.get('head_block_num_operations_inspection')\
        or echo_head_block_num - 1
    if isinstance(inspection_head_block_num, bytes):
        inspection_head_block_num = int(inspection_head_block_num)

    if inspection_head_block_num != echo_head_block_num:
        logs = {}
        for block_num in range(inspection_head_block_num + 1, echo_head_block_num + 1):
            inspection_result = inspect_block_for_committee_operations(block_num)
            if inspection_result:
                logs.update({block_num: inspection_result})

        redis_client.set(
            'head_block_num_operations_inspection',
            block_num,
            ex=2147483647
        )

        if logs:
            influxdb_client = get_influxdb_client()
            influxdb_points = []
            for block_num in logs:
                block_logs = logs[block_num]
                for log_time in block_logs:
                    operations_list = block_logs[log_time]
                    influxdb_points.extend(
                        [
                            {
                                'measurement': 'message_log',
                                'time': log_time,
                                'fields': {
                                    'value': str(operation)
                                }
                            }
                            for operation in operations_list
                        ]
                    )
            influxdb_client.write_points(influxdb_points)
