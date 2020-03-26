from flask import Flask
from utils import initialize_celery
from api import pc, get_cpu, get_ram, get_free_space, get_external_ip,\
    exchange, get_eth_rate, get_btc_rate, node, get_logs
from config import REDIS_HOST, REDIS_PORT, CELERY_REDIS_DATABASE
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec


app = Flask(__name__)


celery_redis_url = 'redis://{}:{}/{}'.format(
    REDIS_HOST,
    REDIS_PORT,
    CELERY_REDIS_DATABASE
)

app.config.update(
    CELERY_BROKER_URL=celery_redis_url,
    CELERY_RESULT_BACKEND=celery_redis_url
)

celery_beat_schedule = {
    'update-pc-information': {
        'task': 'tasks.pc.update_pc_information',
        'schedule': 60.
    },
    'update-exchange-information': {
        'task': 'tasks.rate.update_currencies_rate',
        'schedule': 60.
    },
    'update-node-information': {
        'task': 'tasks.node.update_node_information',
        'schedule': 10.
    },
}

celery_include = [
    'tasks.pc',
    'tasks.rate',
    'tasks.node',
]

celery = initialize_celery(
    app,
    celery_beat_schedule,
    celery_include
)


app.config.update({
    'APISPEC_SPEC': APISpec(
        title='PC',
        version='v1',
        openapi_version="3.0.2",
        plugins=[MarshmallowPlugin()],
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',
})

docs = FlaskApiSpec(app)

app.register_blueprint(pc)
docs.register(get_cpu, blueprint='pc')
docs.register(get_ram, blueprint='pc')
docs.register(get_free_space, blueprint='pc')
docs.register(get_external_ip, blueprint='pc')

app.register_blueprint(exchange)
docs.register(get_eth_rate, blueprint='exchange')
docs.register(get_btc_rate, blueprint='exchange')

app.register_blueprint(node)
docs.register(get_logs, blueprint='node')
