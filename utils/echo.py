import os
import math
from datetime import datetime
from glob import glob
from echopy import Echo
from config import ECHO_URL


def get_echo_client():
    echo = Echo()
    echo.connect(ECHO_URL)
    return echo


def get_echo_head_block_num():
    echo = get_echo_client()
    return echo.api.database.get_dynamic_global_properties()['head_block_number']


def get_echo_node_uptime():
    logs_creation_datetime = datetime.fromtimestamp(
        os.path.getctime('echo-logs')
    )
    current_datetime = datetime.now()
    timedelta = current_datetime - logs_creation_datetime
    return timedelta.total_seconds() / 86400


def _initialize_echo_committee_operations():
    echo = get_echo_client()
    committee_operations = [
        echo.config.operation_ids.COMMITTEE_MEMBER_CREATE,
        echo.config.operation_ids.COMMITTEE_MEMBER_UPDATE,
        echo.config.operation_ids.COMMITTEE_MEMBER_UPDATE_GLOBAL_PARAMETERS,
        echo.config.operation_ids.COMMITTEE_MEMBER_ACTIVATE,
        echo.config.operation_ids.COMMITTEE_MEMBER_DEACTIVATE,
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
    return echo, committee_operations


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


def inspect_block_for_committee_operations(block_num):
    echo, committee_operations = _initialize_echo_committee_operations()
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


def _get_date(date):
    date = datetime.fromisoformat(date)
    return date.strftime("%Y%m%dT%H")


def _compare_date(date, first_log):
    first_log = first_log[first_log.rfind("."):]
    first_log_date = datetime.strptime(first_log, "%Y%m%dT%H%M%S")
    date = datetime.fromisoformat(date)
    return first_log_date < date


def get_echo_logs(logs_dir, logs_from=None, length=math.inf):
    logs_files = glob('./echo-logs/{}/*'.format(logs_dir))
    logs_files.sort()
    logs = []
    logs_files = logs_files[1:]
    if logs_from and _compare_date(logs_files[0]):
        logs_from = _get_date(logs_from)
        for idx, log in enumerate(logs_files):
            if logs_from in log:
                logs_files = logs_files[idx:]
    for i in range(len(logs_files)):
        logs_file = open(logs_files[-(1 + i)])
        lines = logs_file.readlines()
        if length < len(lines):
            lines = lines[len(lines) - length:]
            lines.extend(logs)
            logs = lines
            break
        length -= len(lines)
        lines.extend(logs)
        logs = lines
    return logs
