import unittest
import redis

from rq import SimpleWorker, Queue

from config import app, db
from models import Counter
from utils import count_words_at_url

r = redis.Redis('localhost')
queue = Queue(connection = r)


class CounterTest(unittest.TestCase):

	def setUp(self):
		app.config['TESING'] = True
		self.app = app.test_client()
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
		# self.app.config()
		self.worker = SimpleWorker([queue], connection=queue.connection)

		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.worker.work(burst=True)



	def test_flask_application_is_up_and_running(self):
		response = self.app.get('/')
		self.assertEqual(response.status_code, 200)

	def test_redis_server_is_up_and_running(self):
		response = r.ping()
		self.assertEqual(response, True)

	def test_redis_worker(self):
		self.assertEqual(self.worker.get_state(), 'starting')

	def test_can_create_job(self):
		job = queue.enqueue(count_words_at_url, 'https://edyst.com/')
		self.assertEqual(job.is_queued, True)

	def test_successful_result(self):
		url = 'https://srinandan33.github.io'
		instance_id = count_words_at_url(url)
		instance = Counter.query.filter_by(url=url).first()
		self.assertEqual(instance.word_count,128)

	

if __name__ == '__main__':
	unittest.main()