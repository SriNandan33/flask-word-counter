import unittest
import redis

from flask import Flask
from rq import SimpleWorker, Queue

from app import app, count_words_at_url

r = redis.Redis('localhost')
queue = Queue(connection = r)


class CounterTest(unittest.TestCase):

	def setUp(self):
		app.config['TESING'] = True
		self.app = app.test_client()

	def test_flask_application_is_up_and_running(self):
		response = self.app.get('/')
		self.assertEqual(response.status_code, 200)

	def test_redis_server_is_up_and_running(self):
		response = r.ping()
		self.assertEqual(response, True)

	def test_redis_worker(self):
		worker = SimpleWorker([queue], connection=queue.connection)
		self.assertEqual(worker.get_state(), 'starting')
		worker.work(burst=True)

	def test_can_create_job(self):
		job = queue.enqueue(count_words_at_url, 'https://edyst.com/')
		self.assertEqual(job.is_queued, True)


	

if __name__ == '__main__':
	unittest.main()