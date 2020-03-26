from flask import Blueprint, jsonify
from api.models import PC_cpu, PC_ram
from flask_apispec import use_kwargs, marshal_with, doc
from utils import get_redis_client, get_influxdb_client
from datetime import datetime, timedelta

pc = Blueprint('pc', 'pc', url_prefix='/api/pc')


@doc(tags=['PC'])
@pc.route('/cpu', methods=['GET'])
@use_kwargs(PC_cpu, locations=['querystring'])
@marshal_with(PC_cpu, code=200)
def get_cpu(**kwargs):
    cli = get_influxdb_client()
    time = datetime.utcnow() - timedelta(hours=kwargs['hours'])
    time = time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    query = cli.query("select * from cpu where time >= '{}'".format(time))
    return jsonify({'message': query.raw['series'][0]["values"]})


@doc(tags=['PC'])
@pc.route('/ram', methods=['GET'])
@use_kwargs(PC_ram, locations=['querystring'])
@marshal_with(PC_ram, code=200)
def get_ram(**kwargs):
    cli = get_influxdb_client()
    time = datetime.utcnow() - timedelta(hours=kwargs['hours'])
    time = time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    query = cli.query("select * from ram where time >= '{}'".format(time))
    return jsonify({'message': query.raw['series'][0]["values"]})


@doc(tags=['PC'])
@pc.route('/free-space', methods=['GET'])
def get_free_space():
    cli = get_redis_client()
    query = cli.get('free_space').decode('utf-8')
    return jsonify({'message': query})


@doc(tags=['PC'])
@pc.route('/external-ip', methods=['GET'])
def get_external_ip():
    cli = get_redis_client()
    query = cli.get('public_ip').decode('utf-8')
    return jsonify({'message': query})
