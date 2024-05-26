from redis import StrictRedis
from settings import DEBUG
from os import getenv


if DEBUG:
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
else:
    REDIS_HOST = getenv("REDIS_HOST") or "localhost"
    REDIS_PORT = getenv("REDIS_PORT") or 6379


redis_connection = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
