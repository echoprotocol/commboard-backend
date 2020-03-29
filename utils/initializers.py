from celery import Celery
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from config import REDIS_HOST, REDIS_PORT, CELERY_REDIS_DATABASE


# Flask app

def register_app_blueprints(app, blueprints):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
    return app


# Celery

def update_app_celery_config(app):
    celery_redis_url = 'redis://{}:{}/{}'.format(
        REDIS_HOST,
        REDIS_PORT,
        CELERY_REDIS_DATABASE
    )

    app.config.update(
        CELERY_BROKER_URL=celery_redis_url,
        CELERY_RESULT_BACKEND=celery_redis_url
    )
    return app


def initialize_celery(app):
    celery_beat_schedule = {
        'update-pc-information': {
            'task': 'tasks.pc.update_pc_information',
            'schedule': 60.
        },
        'update-exchange-information': {
            'task': 'tasks.rate.update_currencies_rate',
            'schedule': 600.
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

    celery = Celery(app.name)

    celery.conf.update(
        broker_url=app.config['CELERY_BROKER_URL'],
        result_backend=app.config['CELERY_RESULT_BACKEND'],
        timezone='UTC',
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        beat_schedule=celery_beat_schedule,
        include=celery_include,
    )

    return celery


# Apispec

def update_app_apispec_config(app):
    app.config.update({
        'APISPEC_SPEC': APISpec(
            title='Committee Dashboard API',
            version='0.0.1',
            openapi_version='2.0',
            plugins=[MarshmallowPlugin()],
        ),
        'APISPEC_SWAGGER_URL': '/api/swagger/',
        'APISPEC_SWAGGER_UI_URL': '/api/'
    })
    return app


def initialize_apispec(app):
    return FlaskApiSpec(app)


def register_apispec_methods(apispec, methods, blueprint):
    for method in methods:
        apispec.register(method, blueprint=blueprint)

    return apispec


def remove_options_from_apispec(apispec):
    for key, value in apispec.spec._paths.items():
        apispec.spec._paths[key] = {
            inner_key: inner_value
            for inner_key, inner_value in value.items()
            if inner_key != 'options'
        }
    return apispec
