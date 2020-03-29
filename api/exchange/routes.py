from flask import Blueprint
from utils import get_redis_client
from flask_apispec import doc, marshal_with
from api.models import GetRatesResponse, GetNullResponse, ErrorStringResponse


exchange = Blueprint('exchange', 'exchange', url_prefix='/api/exchange')


@exchange.route('/get-rates/', methods=['GET'])
@doc(tags=['exchange'], description='Get latest rates')
@marshal_with(GetRatesResponse, code=200)
@marshal_with(GetNullResponse, code=204)
@marshal_with(ErrorStringResponse, code=503)
def get_rates():
    try:
        redis_client = get_redis_client()
    except Exception:
        return ErrorStringResponse().load(
            {'error': 'Error with database connection'}), 503

    btc = redis_client.get('btc')
    eth = redis_client.get('eth')

    status_code = 200
    if btc is None or eth is None:
        status_code = 204

    if isinstance(btc, bytes):
        btc = btc.decode()
    if isinstance(eth, bytes):
        eth = eth.decode()

    response = GetRatesResponse().load(
        {'message': {'BTC': btc, 'ETH': eth}})

    return response, status_code
