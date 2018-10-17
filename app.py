import requests
import redis

from wordcounter import app


if __name__ == '__main__':
	app.run(debug=True)