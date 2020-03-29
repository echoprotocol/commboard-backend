import os
import math
from datetime import datetime
from glob import glob
from echopy import Echo
from config import ECHO_URL
import re


def get_echo_client():
    echo = Echo()
    echo.connect(ECHO_URL)
    return echo


def get_echo_head_block_num(echo, timestamp=False):
    dynamic_global_properties = echo.api.database.get_dynamic_global_properties()
    if timestamp:
        return dynamic_global_properties['head_block_number'], dynamic_global_properties['time']
    return dynamic_global_properties['head_block_number']


def get_echo_active_committee_members(echo):
    return echo.api.database.get_global_properties()['active_committee_members']


def get_echo_node_uptime():
    logs_creation_datetime = datetime.fromtimestamp(
        os.path.getctime('echo-logs')
    )
    current_datetime = datetime.now()
    timedelta = current_datetime - logs_creation_datetime
    return timedelta.total_seconds() / 86400


def _initialize_echo_committee_operations(echo):
    committee_operations = [
        echo.config.operation_ids.COMMITTEE_MEMBER_CREATE,
        echo.config.operation_ids.COMMITTEE_MEMBER_UPDATE,
        echo.config.operation_ids.COMMITTEE_MEMBER_UPDATE_GLOBAL_PARAMETERS,
        # echo.config.operation_ids.COMMITTEE_MEMBER_ACTIVATE,
        # echo.config.operation_ids.COMMITTEE_MEMBER_DEACTIVATE,
        echo.config.operation_ids.COMMITTEE_FROZEN_BALANCE_DEPOSIT,
        echo.config.operation_ids.COMMITTEE_FROZEN_BALANCE_WITHDRAW,
        echo.config.operation_ids.PROPOSAL_CREATE,
        echo.config.operation_ids.SIDECHAIN_ETH_APPROVE_ADDRESS,
        echo.config.operation_ids.SIDECHAIN_ETH_DEPOSIT,
        echo.config.operation_ids.SIDECHAIN_ETH_SEND_DEPOSIT,
        echo.config.operation_ids.SIDECHAIN_ETH_SEND_WITHDRAW,
        echo.config.operation_ids.SIDECHAIN_ETH_APPROVE_WITHDRAW,
        echo.config.operation_ids.SIDECHAIN_ERC20_DEPOSIT_TOKEN,
        echo.config.operation_ids.SIDECHAIN_ERC20_SEND_DEPOSIT_TOKEN,
        echo.config.operation_ids.SIDECHAIN_ERC20_SEND_WITHDRAW_TOKEN,
        echo.config.operation_ids.SIDECHAIN_ERC20_APPROVE_TOKEN_WITHDRAW,
        echo.config.operation_ids.SIDECHAIN_BTC_CREATE_INTERMEDIATE_DEPOSIT,
        echo.config.operation_ids.SIDECHAIN_BTC_INTERMEDIATE_DEPOSIT,
        echo.config.operation_ids.SIDECHAIN_BTC_DEPOSIT,
        echo.config.operation_ids.SIDECHAIN_BTC_AGGREGATE,
        echo.config.operation_ids.SIDECHAIN_BTC_APPROVE_AGGREGATE
    ]
    return committee_operations


def _inspect_operation(echo, full_operation, committee_operations):
    operation_id, operation = full_operation
    if operation_id in committee_operations:
        if operation_id == echo.config.operation_ids.PROPOSAL_CREATE:
            result_operations = []
            for op in operation['proposed_ops']:
                inspection_result = _inspect_operation(
                    echo,
                    op['op'],
                    committee_operations
                )
                if inspection_result:
                    result_operations.extend(inspection_result)
            return result_operations
        return [full_operation]
    return []


def inspect_block_for_committee_operations(echo, block_num):
    committee_operations = _initialize_echo_committee_operations(echo)
    block = echo.api.database.get_block(block_num)
    block_timestamp = block['timestamp']
    logs = []
    result = {}
    for tx in block['transactions']:
        for operation in tx['operations']:
            inspection_result = _inspect_operation(
                echo,
                operation,
                committee_operations
            )
            logs.extend(inspection_result)
    if logs:
        result.update({block_timestamp: logs})
    return result


def _compare_committee_members_lists(current, latest):
    latest_set = set(latest)
    current_set = set(current)
    kicked = latest_set - current_set
    new = current_set - latest_set
    return kicked, new


def check_active_committee_members_update(echo, timestamp, latest_active_committee_members,
                                          current_active_committee_members):
    kicked_committee_members, new_committee_members = _compare_committee_members_lists(
        current_active_committee_members,
        latest_active_committee_members
    )

    logs = {}
    if kicked_committee_members:
        logs.update({timestamp: 'Removed from active committee members list: {}'.format(kicked_committee_members)})

    if new_committee_members:
        logs.update({timestamp: 'Added to active committee members list: {}'.format(new_committee_members)})

    return logs


def _get_date(date):
    return date.strftime('%Y%m%dT%H')


def _get_time(date):
    return date.strftime('%H:%M:%S')


def _compare_date(date, first_log):
    first_log = first_log[first_log.rfind('.') + 1:]
    first_log_date = datetime.strptime(first_log, '%Y%m%dT%H%M%S')
    return first_log_date < date


def binary_search(logs, time, position=0, temp_value=0):
    if not position:
        position += len(logs) // 2
        temp_value = position // 2 + 1
        time = datetime.strptime(time, '%H:%M:%S')
    time_from_logs = logs[position][:logs[position].find('.')]
    time_from_logs = datetime.strptime(time_from_logs, '%H:%M:%S')

    if time_from_logs > time:
        position -= temp_value
        temp_value = len(logs[position:position + temp_value]) // 2
        if temp_value == 1:
            return position + 1
        return binary_search(logs, time, position, temp_value)

    elif time_from_logs < time:
        position += temp_value
        temp_value = len(logs[position - temp_value:position]) // 2
        if temp_value == 1:
            return position + 1
        return binary_search(logs, time, position, temp_value)

    else:
        time_from_logs = logs[position][:logs[position].find('.')]
        time_from_logs = datetime.strptime(time_from_logs, '%H:%M:%S')
        while time_from_logs == time:
            position -= 1
            time_from_logs = logs[position][:logs[position].find('.')]
            time_from_logs = datetime.strptime(time_from_logs, '%H:%M:%S')
    return position + 1


def get_echo_logs(logs_dir, hours=None, quantity=math.inf):
    logs_files = glob('./echo-logs/{}/*'.format(logs_dir))
    logs_files.sort()
    first_log = []
    logs = []
    logs_files = logs_files[1:]
    if logs_files:
        if hours and _compare_date(hours, logs_files[0]):
            time = _get_time(hours)
            hours = _get_date(hours)
            time_patern = re.compile('^[0-2][0-9]:[0-5][0-9]:[0-5][0-9]$')
            for idx, log in enumerate(logs_files):
                if hours in log:
                    logs_file = open(log)
                    lines = logs_file.readlines()

                    processed_logs = []

                    for index, log in enumerate(lines):
                        if time_patern.match(log[:8]):
                            processed_logs.append(log)
                            continue
                        processed_logs[-1] += log
                    binc = binary_search(processed_logs, time)
                    first_log = lines[binc:]
                    logs_files = logs_files[idx + 1:]
                    break
        for i in range(len(logs_files)):
            logs_file = open(logs_files[-(1 + i)])
            lines = logs_file.readlines()
            if quantity < len(lines):
                first_log = []
                lines = lines[len(lines) - quantity:]
                lines.extend(logs)
                logs = lines
                break
            quantity -= len(lines)
            lines.extend(logs)
            logs = lines
        if quantity > len(first_log):
            first_log.extend(logs)
            logs = first_log
        else:
            first_log = first_log[len(first_log) - quantity:]
            first_log.extend(logs)
            logs = first_log
    return logs
