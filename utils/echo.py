from echopy import Echo
from config import ECHO_URL


def get_echo_client():
    echo = Echo()
    echo.connect(ECHO_URL)
    return echo


def initialize_echo_committee_operations():
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


def inspect_operation(echo, full_operation, committee_operations):
    operation_id, operation = full_operation
    if operation_id in committee_operations:
        if operation_id == echo.config.operation_ids.PROPOSAL_CREATE:
            result_operations = []
            for op in operation['proposed_ops']:
                inspection_result = inspect_operation(echo, op["op"], committee_operations)
                if inspection_result:
                    result_operations.extend(inspection_result)
            return result_operations
        return [full_operation]
    return []


def inspect_block_for_committee_operations(block_num):
    echo, committee_operations = initialize_echo_committee_operations()
    block = echo.api.database.get_block(block_num)
    block_timestamp = block['timestamp']
    logs = []
    for tx in block['transactions']:
        for operation in tx['operations']:
            inspection_result = inspect_operation(echo, operation, committee_operations)
            logs.extend(inspection_result)
    if len(logs):
        return {block_timestamp: logs}
    return None
