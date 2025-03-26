import time
from django_redis import get_redis_connection

RATE_LIMIT_WINDOW = 60 # 60 second
RATE_LIMIT = 1000 # 1000 requests allow in 60 seconds

def check_rate_limit(key):
    
    rlkey = "rl:"+key
    now_ts = time.time()
    start_ts = now_ts - RATE_LIMIT_WINDOW
    expiration = RATE_LIMIT_WINDOW + 1

    r = get_redis_connection()
    pipe = r.pipeline()

    results = pipe.zadd(rlkey, {now_ts: now_ts}).\
        zremrangebyscore(rlkey, 0, start_ts).\
            zcard(rlkey).\
                expire(rlkey, 61).execute()

    return int(results[2]) <= RATE_LIMIT
