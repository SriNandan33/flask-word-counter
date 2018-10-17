import requests
from flask import Flask, render_template, redirect, url_for, request
from forms import UrlInputForm
from flask_sqlalchemy import SQLAlchemy
from rq import Queue
from rq.job import Job
from worker import conn


# configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'f97d8be751f31b5f16f143bb9fef833e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///edyst.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
q = Queue(connection=conn)


# database model
class Counter(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	url = db.Column(db.String, nullable=False)
	word_count = db.Column(db.Integer, nullable=False)


	def __repr__(self):
		return '{0} has {1} words'.format(self.url, self.word_count)



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


# views

@app.route('/', methods=['GET', 'POST'])
def home():
	result = None
	form = UrlInputForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			input_url = form.url.data
			job = q.enqueue_call(
            	func='app.count_words_at_url', args=(input_url,), result_ttl=5000
        	)
			return redirect('/results/{0}'.format(job.get_id()))
		else:
			print('form is invalid')

	return render_template('home.html', form=form)


@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):

    job = Job.fetch(job_key, connection=conn)

    if job.is_finished:
    	obj = Counter.query.filter_by(id=job.result).first()
    	print(obj)
    	return str(obj.word_count)
    else:
        return "Please keep refreshing the page to see the results"




if __name__ == '__main__':
	app.run(debug=True)