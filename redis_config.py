import redis

# Establish a connection to Redis
redis_host = 'localhost'  # Redis server host
redis_port = 6379  # Redis server port
redis_db = 'baleli'  # Redis database number as a string
redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

# Rest of the code remains the same
