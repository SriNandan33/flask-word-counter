import requests

from config import db
from models import Counter


# funciton to count the words in a URL and save it to the database
def count_words_at_url(url):
	resp = requests.get(url)
	word_count = len(resp.text.split())
	try:
		instance = Counter(url=url, word_count=word_count)
		db.session.add(instance)
		db.session.commit()
		return instance.id
	except:
		print('not able to insert in db')