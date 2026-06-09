import redis
import time
from django.conf import settings
from django.apps import apps

class RateLimiter:
    def __init__(self, limit_name):
        # See docker-compose.yml

        app_config = apps.get_app_config('rate_limiter')
        self.redis_server_available = app_config.redis_server_available

        # create the redis client if the redis server exists
        if not self.redis_server_available:
            self.limit_tracker = None
        else:
            self.limit_tracker = redis.Redis(
                host="redis", 
                port=6379,
                db=0,
                decode_responses=True,
                socket_connect_timeout=2,
            )

            default_policy = {'rate': 1, 'time_frame': 60}

            self.policy = settings.RATE_LIMIT_POLICIES.get(limit_name, default_policy)
            self.rate =  self.policy['rate']
            self.limit_time = self.policy['limit_time']
            self.limit_name = limit_name

    '''
    Method to enforce rate limits.
    @param key_id, the entity whose actions are being rate limited
    @param limit_name, the limit being enforced
    @param limit_time, the time period for the limit
    @param limit, the count/quantity of the limit for the given time period
    @return True if the rate limit has been reached, otherwise returns False
    If successful, action count and time limit will be adjusted for the new action only until the rate limit is reached
    '''
    #def enforce_rate_limit(self, key_id, limit_name, limit_time, limit):
    def enforce_rate_limit(self, key_id):
        # if the redis server isn't available, skip checking the rate limit
        if not self.redis_server_available:
            return False

        # if the redis server drops mid-deployment, fail safely, ie return False here too
        try:
            self.enforce_rate_limit_helper(key_id)
        except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError) as e:
            print(f"Redis server exception: {e}")
            return False

    def enforce_rate_limit_helper(self, key_id):
        key = self.get_key(key_id, self.limit_name)
        current_time = int(time.time())

        self.remove_expired_count(key, current_time, self.limit_time)

        if self.limit_tracker.zcard(key) >= self.rate:
            print("===> IN IF ", flush=True)
            return True
        
        self.increment_count(key, current_time, self.rate)
        self.set_timer(key, self.limit_time)
        return False


    '''
    Method to get a unique key name
    @param key_id, the entity whose actions are being rate limited (i.e. user id)
    @param limit_name, the limit being enforced
    @return A unique key for the rate being managed
    '''
    def get_key(self, key_id, limit_name):
        return f"{limit_name}:{key_id}"


    '''
    Method to remove expired counts from tracking
    @param: key, the rate being managed
    @param: current_time, the time when latest action was taken
    @param limit_time, the time period for the limit
    If key exists, any expired timestamps are removed from the count, otherwise nothing happens
    '''
    def remove_expired_count(self, key, current_time, limit_time):
        newest_expired = current_time - limit_time
        oldest_expired = 0
        self.limit_tracker.zremrangebyscore(key, oldest_expired, newest_expired)


    '''
    Method to add a count to tracking
    @param: key, the rate being managed
    @param: current_time, the time when latest action was taken
    @param rate, the count/quantity allowed for the given time period
    If successful, rate count is either created or updated with a timestamp for the latest action
    '''
    def increment_count(self, key, current_time, rate):
        #if self.limit_tracker.zcard(key) < rate:
        self.limit_tracker.zadd(key, {str(current_time):current_time})


    '''
    Method to set a timer for tracking
    @param: key, the rate being managed
    @param limit_time, the time period for the limit
    If successful, the timer for an instance to disappear will be added (if instance is new) 
                   or updated (if instance already exists) based on when the latest action was taken
    '''
    def set_timer(self, key, limit_time):
        self.limit_tracker.expire(key, limit_time)