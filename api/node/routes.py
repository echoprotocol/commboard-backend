from flask import Blueprint, jsonify
from api.models import GetEchoLogs
from flask_apispec import use_kwargs, marshal_with, doc
from utils import get_echo_logs

node = Blueprint('node', 'node', url_prefix='/api/node')


@doc(tags=['node'])
@node.route('/get-echo-logs', methods=['GET'])
@use_kwargs(GetEchoLogs, locations=['querystring'])
@marshal_with(GetEchoLogs, code=200)
def get_logs(**kwargs):
    logs = get_echo_logs(**kwargs)
    return jsonify({'message': logs})
