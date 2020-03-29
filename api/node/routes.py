from flask import Blueprint
from api.models import GetEchoLogsRequest, GetEchoLogsResponse, GetMessageLogsRequest, GetMessageLogsResponse,\
    GetUptimeResponse, GetNullResponse, ErrorStringResponse
from flask_apispec import use_kwargs, marshal_with, doc
from utils import get_echo_logs, get_influxdb_client, get_redis_client
from datetime import datetime, timedelta


node = Blueprint('node', 'node', url_prefix='/api/node')


@node.route('/get-logs/', methods=['GET'])
@doc(tags=['node'], description='Get ECHO node logs')
@use_kwargs(GetEchoLogsRequest, locations=['querystring'])
@marshal_with(GetEchoLogsResponse, code=200)
@marshal_with(GetNullResponse, code=422)
def get_logs(**kwargs):
    data = GetEchoLogsRequest().load(kwargs)
    if 'hours' in data:
        data['hours'] = datetime.utcnow() - timedelta(hours=kwargs['hours'])
    logs = get_echo_logs(**data)

    response = GetEchoLogsResponse().load(
        {'message': logs})
    return response, 200


@node.route('/get-message-logs/', methods=['GET'])
@doc(tags=['node'], description='Get ECHO node message logs')
@use_kwargs(GetMessageLogsRequest, locations=['querystring'])
@marshal_with(GetMessageLogsResponse, code=200)
@marshal_with(GetNullResponse, code=422)
@marshal_with(ErrorStringResponse, code=503)
def get_message_logs(**kwargs):
    data = GetMessageLogsRequest().load(kwargs)

    try:
        influxdb_client = get_influxdb_client()
    except Exception:
        return ErrorStringResponse().load(
            {'error': 'Error with database connection'}), 503

    query_where = query_limit = ''
    if 'hours' in data:
        time = datetime.utcnow() - timedelta(hours=data['hours'])
        time = time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        query_where = " where time >= '{}'".format(time)

    if 'quantity' in data:
        query_limit = ' limit {}'.format(data['quantity'])

    logs = influxdb_client.query(
        'select * from message_log{}{}'.format(
            query_where,
            query_limit
        )
    ).raw

    logs = [] if 'series' not in logs else logs['series'][0]['values']

    response = GetMessageLogsResponse().load({
        'message': {
            time: value
            for (time, value)
            in logs
        }
    })

    return response, 200


@node.route('/get-uptime/', methods=['GET'])
@doc(tags=['node'], description='Get ECHO node uptime')
@marshal_with(GetUptimeResponse, code=200)
@marshal_with(GetNullResponse, code=204)
@marshal_with(ErrorStringResponse, code=503)
def get_uptime(**kwargs):
    try:
        redis_client = get_redis_client()
    except Exception:
        return ErrorStringResponse().load(
            {'error': 'Error with database connection'}), 503

    uptime = redis_client.get('uptime')

    status_code = 200
    if uptime is None:
        status_code = 204

    if isinstance(uptime, bytes):
        uptime = uptime.decode()

    response = GetUptimeResponse().load(
        {'message': uptime})
    return response, status_code
