import os
import redis

def redis_client():
    return redis.StrictRedis(host="redishost", port= 6379, db = 0)
