import redis
import time

# 86400 = 1 day
SUGGESTION_TIME_FRAME = 86400
SUGGESTION_RATE_LIMIT = 3

#Tracks counts for resident idea suggestions
suggestion_tracker = redis.Redis(
    host="redis", #as per docker-compose.yml
    port=6379,
    db=0
)

'''
Method to enforce rate limits
@param user_id, the user whose actions are being rate limited
@param limit_name, the limit being enforced
@return True if the user has hit their rate limit, otherwise False
'''
def enforce_rate_limit(user_id, limit_name):
    #1. Make a key, get current time
    key = f"{limit_name}:{user_id}"
    current_time = int(time.time())

    update_usage_count(key, current_time)
    suggestion_tracker.expire(key, SUGGESTION_TIME_FRAME)

    if suggestion_tracker.zcard(key) > SUGGESTION_RATE_LIMIT:
        print("AT LIMIT")
        return True
    else:
        print("NOT AT LIMIT")
        return False

'''
Method to update the user's usage counts
@param: key, the user
@param: time, the current time
If successful, user count is either created or updated with a timestamp for their latest action
               and any expired timestamps are removed from user's count
'''
def update_usage_count(key, current_time):
    newest_expired = current_time - SUGGESTION_TIME_FRAME
    oldest_expired = 0
    suggestion_tracker.zremrangebyscore(key, oldest_expired, newest_expired)

    if suggestion_tracker.zcard(key) < SUGGESTION_RATE_LIMIT:
        suggestion_tracker.zadd(key, {str(current_time):current_time})
    