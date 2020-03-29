from flask import Blueprint
from api.models import GetCpuHistoryRequest, GetCpuHistoryResponse, GetRamHistoryRequest, GetRamHistoryResponse,\
    GetFreeSpaceResponse, GetExternalIpResponse, GetNullResponse, ErrorStringResponse
from flask_apispec import use_kwargs, marshal_with, doc
from utils import get_redis_client, get_influxdb_client
from datetime import datetime, timedelta


pc = Blueprint('pc', 'pc', url_prefix='/api/pc')


@pc.route('/get-cpu-history/', methods=['GET'])
@doc(tags=['pc'], description='Get history of CPU busy')
@use_kwargs(GetCpuHistoryRequest, locations=['querystring'])
@marshal_with(GetCpuHistoryResponse, code=200)
@marshal_with(ErrorStringResponse, code=400)
@marshal_with(GetNullResponse, code=422)
@marshal_with(ErrorStringResponse, code=503)
def get_cpu_history(**kwargs):
    data = GetCpuHistoryRequest().load(kwargs)

    if data['hours'] < 1:
        return ErrorStringResponse().load(
            {'error': 'Hours must be greater greater than 0'}), 400

    try:
        influxdb_client = get_influxdb_client()
    except Exception:
        return ErrorStringResponse().load(
            {'error': 'Error with database connection'}), 503

    time = datetime.utcnow() - timedelta(hours=data['hours'])
    time = time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    cpu_history_result = influxdb_client.query(
        "select * from cpu where time >= '{}'".format(time)
    ).raw

    cpu_history_result = [] if 'series' not in cpu_history_result\
        else cpu_history_result['series'][0]['values']

    response = GetCpuHistoryResponse().load({
        'message': {
            time: value
            for (time, value)
            in cpu_history_result
        }
    })

    return response, 200


@pc.route('/get-ram-history/', methods=['GET'])
@doc(tags=['pc'], description='Get history of RAM busy')
@use_kwargs(GetRamHistoryRequest, locations=['querystring'])
@marshal_with(GetRamHistoryResponse, code=200)
@marshal_with(ErrorStringResponse, code=400)
@marshal_with(GetNullResponse, code=422)
@marshal_with(ErrorStringResponse, code=503)
def get_ram_history(**kwargs):
    data = GetRamHistoryRequest().load(kwargs)

    if data['hours'] < 1:
        return ErrorStringResponse().load(
            {'error': 'Hours must be greater than 0'}), 400

    try:
        influxdb_client = get_influxdb_client()
    except Exception:
        return ErrorStringResponse().load(
            {'error': 'Error with database connection'}), 503

    time = datetime.utcnow() - timedelta(hours=data['hours'])
    time = time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    ram_history_result = influxdb_client.query(
        "select * from ram where time >= '{}'".format(time)
    ).raw

    ram_history_result = [] if 'series' not in ram_history_result\
        else ram_history_result['series'][0]['values']

    response = GetRamHistoryResponse().load({
        'message': {
            time: value
            for (time, value)
            in ram_history_result
        }
    })

    return response, 200


@pc.route('/get-free-space/', methods=['GET'])
@doc(tags=['pc'], description='Get amount of free space')
@marshal_with(GetFreeSpaceResponse, code=200)
@marshal_with(GetNullResponse, code=204)
@marshal_with(ErrorStringResponse, code=503)
def get_free_space():
    try:
        redis_client = get_redis_client()
    except Exception:
        return ErrorStringResponse().load(
            {'error': 'Error with database connection'}), 503

    free_space = redis_client.get('free_space')

    status_code = 200
    if free_space is None:
        status_code = 204

    if isinstance(free_space, bytes):
        free_space = free_space.decode()

    response = GetFreeSpaceResponse().load(
        {'message': free_space})

    return response, status_code


@pc.route('/get-external-ip/', methods=['GET'])
@doc(tags=['pc'], description='Get external ip')
@marshal_with(GetExternalIpResponse, code=200)
@marshal_with(GetNullResponse, code=204)
@marshal_with(ErrorStringResponse, code=503)
def get_external_ip():
    try:
        redis_client = get_redis_client()
    except Exception:
        return ErrorStringResponse().load(
            {'error': 'Error with database connection'}), 503

    external_ip = redis_client.get('external_ip')

    status_code = 200
    if external_ip is None:
        status_code = 204

    if isinstance(external_ip, bytes):
        external_ip = external_ip.decode()

    response = GetExternalIpResponse().load(
        {'message': external_ip})
    return response, status_code
