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
