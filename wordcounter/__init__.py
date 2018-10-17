import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from rq import Queue

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f97d8be751f31b5f16f143bb9fef833e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///edyst.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

redis_conn = redis.StrictRedis(host='localhost', port=6379, db=12)
queue = Queue(connection=redis_conn)
from wordcounter import views


