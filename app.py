from flask import Flask
from utils.db import initialize_influxdb_database
from utils.celery import initialize_celery
from config import REDIS_HOST, REDIS_PORT, CELERY_REDIS_DATABASE


initialize_influxdb_database()

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
        'schedule': 10.
    }
}
celery_include = [
    'tasks.pc'
]

celery = initialize_celery(
    app,
    celery_beat_schedule,
    celery_include
)


@app.route('/')
def hello_world():
    return('Hello, World!')
