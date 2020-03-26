import os

if 'DATABASE_NAME' not in os.environ:
    raise Exception("Not found 'DATABASE_NAME' in environment")
DATABASE_NAME = os.environ['DATABASE_NAME']

if 'DATABASE_USER_NAME' not in os.environ:
    raise Exception("Not found 'DATABASE_USER_NAME' in environment")
DATABASE_USER_NAME = os.environ['DATABASE_USER_NAME']

if 'DATABASE_USER_PASSWORD' not in os.environ:
    raise Exception("Not found 'DATABASE_USER_PASSWORD' in environment")
DATABASE_USER_PASSWORD = os.environ['DATABASE_USER_PASSWORD']

if 'DATABASE_HOST' not in os.environ:
    raise Exception("Not found 'DATABASE_HOST' in environment")
DATABASE_HOST = os.environ['DATABASE_HOST']

if 'DATABASE_PORT' not in os.environ:
    raise Exception("Not found 'DATABASE_PORT' in environment")
DATABASE_PORT = os.environ['DATABASE_PORT']

if 'REDIS_HOST' not in os.environ:
    raise Exception("Not found 'REDIS_HOST' in environment")
REDIS_HOST = os.environ['REDIS_HOST']

if 'REDIS_PORT' not in os.environ:
    raise Exception("Not found 'REDIS_PORT' in environment")
REDIS_PORT = os.environ['REDIS_PORT']

if 'REDIS_DATABASE' not in os.environ:
    raise Exception("Not found 'REDIS_DATABASE' in environment")
REDIS_DATABASE = os.environ['REDIS_DATABASE']

if 'CELERY_REDIS_DATABASE' not in os.environ:
    raise Exception("Not found 'CELERY_REDIS_DATABASE' in environment")
CELERY_REDIS_DATABASE = os.environ['CELERY_REDIS_DATABASE']

COINMARKETCAP_API_URL = 'https://pro-api.coinmarketcap.com/v1/'

if 'COINMARKETCAP_API_KEY' not in os.environ:
    raise Exception("Not found 'COINMARKETCAP_API_KEY' in environment")
COINMARKETCAP_API_KEY = os.environ['COINMARKETCAP_API_KEY']

if 'ECHO_URL' not in os.environ:
    raise Exception("Not found 'ECHO_URL' in environment")
ECHO_URL = os.environ['ECHO_URL']
