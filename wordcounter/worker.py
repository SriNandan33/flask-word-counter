import redis

from rq import Worker, Queue, Connection
listen = ['default']

# redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
# conn = redis.from_url(redis_url)

redis_conn = redis.StrictRedis(host='localhost', port=6379, db=12)

if __name__ == '__main__':
    with Connection(redis_conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()