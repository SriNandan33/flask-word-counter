from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from rq import Queue
from worker import conn


app = Flask(__name__)
app.config['SECRET_KEY'] = 'f97d8be751f31b5f16f143bb9fef833e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///edyst.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
q = Queue(connection=conn)

from views import *