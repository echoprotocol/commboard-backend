from influxdb import InfluxDBClient
from redis import Redis
from config import DATABASE_HOST, DATABASE_PORT, DATABASE_USER_NAME, DATABASE_USER_PASSWORD, DATABASE_NAME,\
    REDIS_HOST, REDIS_PORT, REDIS_DATABASE


def get_influxdb_client():
    influxdb_client = InfluxDBClient(
        DATABASE_HOST,
        DATABASE_PORT,
        DATABASE_USER_NAME,
        DATABASE_USER_PASSWORD,
        DATABASE_NAME
    )
    influxdb_client.ping()
    return influxdb_client


def get_redis_client():
    redis_client = Redis(
        REDIS_HOST,
        REDIS_PORT,
        REDIS_DATABASE
    )
    redis_client.ping()
    return redis_client
