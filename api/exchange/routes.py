from flask import Blueprint, jsonify
from utils import get_redis_client
from flask_apispec import doc
exchange = Blueprint('exchange', 'exchange', url_prefix='/api/exchange')


@doc(tags=['Exchange'])
@exchange.route('/eth-rate', methods=['GET'])
def get_eth_rate():
    cli = get_redis_client()
    query = cli.get('eth').decode('utf-8')
    return jsonify({'message': query})


@doc(tags=['Exchange'])
@exchange.route('/btc-rate', methods=['GET'])
def get_btc_rate():
    cli = get_redis_client()
    query = cli.get('btc').decode('utf-8')
    return jsonify({'message': query})
