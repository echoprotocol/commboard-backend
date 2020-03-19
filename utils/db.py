from influxdb import InfluxDBClient
from redis import Redis
from config import DATABASE_HOST, DATABASE_PORT, DATABASE_USER_NAME, DATABASE_USER_PASSWORD, DATABASE_NAME,\
    REDIS_HOST, REDIS_PORT, REDIS_DATABASE


def get_influxdb_client():
    return InfluxDBClient(
        DATABASE_HOST,
        DATABASE_PORT,
        DATABASE_USER_NAME,
        DATABASE_USER_PASSWORD,
        DATABASE_NAME
    )


def get_redis_client():
    return Redis(
        REDIS_HOST,
        REDIS_PORT,
        REDIS_DATABASE
    )
