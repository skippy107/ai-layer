import os
import redis

class NoSQLClient(object):
    def __new__(cls, **kwargs):

        return redis.Redis(kwargs, host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'))
