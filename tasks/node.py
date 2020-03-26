import json
from utils import get_redis_client, get_influxdb_client, get_echo_node_uptime,\
    get_echo_client, get_echo_head_block_num, inspect_block_for_committee_operations,\
    get_echo_active_committee_members, check_active_committee_members_update
from app import celery


def make_message_log_point(time, value):
    return {
        'measurement': 'message_log',
        'time': time,
        'fields': {
            'value': str(value)
        }
    }


@celery.task()
def update_node_information():
    influxdb_points = []
    node_uptime = get_echo_node_uptime()
    redis_client = get_redis_client()
    redis_client.set(
        'uptime',
        node_uptime
    )

    # operations checking
    echo_client = get_echo_client()
    echo_head_block_num, echo_head_block_timestamp = get_echo_head_block_num(echo_client, True)
    inspection_head_block_num = redis_client.get('head_block_num_operations_inspection')\
        or echo_head_block_num - 1
    if isinstance(inspection_head_block_num, bytes):
        inspection_head_block_num = int(inspection_head_block_num)

    if inspection_head_block_num != echo_head_block_num:
        logs = {}
        for block_num in range(inspection_head_block_num + 1, echo_head_block_num + 1):
            inspection_result = inspect_block_for_committee_operations(
                echo_client,
                block_num
            )
            if inspection_result:
                logs.update(inspection_result)

        redis_client.set(
            'head_block_num_operations_inspection',
            block_num,
            ex=2147483647
        )
        if logs:
            for log_time, operations_list in logs.items():
                influxdb_points.extend(
                    [
                        make_message_log_point(log_time, operation)
                        for operation in operations_list
                    ]
                )

    # events (active committee members updating)
    current_active_committee_members = [
        active_committee_member[0]
        for active_committee_member
        in get_echo_active_committee_members(echo_client)
    ]
    latest_active_committee_members = redis_client.get('latest_active_committee_members')
    if latest_active_committee_members:
        latest_active_committee_members = json.loads(latest_active_committee_members)

        logs = check_active_committee_members_update(
            echo_client,
            echo_head_block_timestamp,
            latest_active_committee_members,
            current_active_committee_members,
        )
        influxdb_points.extend(
            [
                make_message_log_point(log_time, log)
                for log_time, log in logs.items()
            ]
        )
    redis_client.set(
        'latest_active_committee_members',
        json.dumps(current_active_committee_members)
    )

    if influxdb_points:
        influxdb_client = get_influxdb_client()
        influxdb_client.write_points(influxdb_points)
