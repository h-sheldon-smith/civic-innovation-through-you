from django.apps import AppConfig
import redis

class RateLimiterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rate_limiter'

    redis_server_available = False

    def ready(self):
        # create a redis client to test if the redis server exists and set the global flag
        
        import sys
        if 'manage.py' in sys.argv and any(cmd in sys.argv for cmd in ['makemigrations', 'migrate', 'collectstatic']):
            return
        
        limit_tracker = redis.Redis(
            host="redis", 
            port=6379,
            db=0,
            decode_responses=True,
            socket_connect_timeout=2,
        )

        try:
            limit_tracker.ping()
            self.redis_server_available = True
        except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError):
            self.redis_server_available = False
            print("Redis not detected at startup. Rate limiting bypassed globally.")
