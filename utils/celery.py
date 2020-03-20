from celery import Celery


def initialize_celery(app, celery_beat_schedule, include):
    celery = Celery(app.name)

    celery.conf.update(
        broker_url=app.config['CELERY_BROKER_URL'],
        result_backend=app.config['CELERY_RESULT_BACKEND'],
        timezone='UTC',
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        beat_schedule=celery_beat_schedule,
        include=include,
    )

    return celery
