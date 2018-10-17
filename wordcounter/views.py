import requests
import redis
from rq import Queue

def count_words_at_url(url):
	print('counting')
	resp = requests.get(url)
	word_count = len(resp.text.split())
	try:
		instance = Counter(url=url, word_count=word_count)
		db.session.add(instance)
		db.session.commit()
		print('saved in database')
		return instance.id
	except:
		print('not able to insert in db')


from flask import Flask, render_template, redirect, url_for, request
from rq.job import Job


## forms
# from wordcounter.forms import UrlInputForm
from flask_wtf import FlaskForm
from flask_wtf.html5 import URLField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, url


class UrlInputForm(FlaskForm):
	url = URLField('url', validators=[DataRequired(), url() ])
	submit = SubmitField('submit')


from wordcounter import db,app, queue,redis_conn
from wordcounter.models import Counter
@app.route('/', methods=['GET', 'POST'])
def home():
	result = None
	form = UrlInputForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			input_url = form.url.data
			# word_count = count_words_at_url(form.url.data)
			job = queue.enqueue_call(func='views.count_words_at_url',
               args=(input_url,), 
               timeout=10)
			print(job.get_id())
			return redirect('/results/{0}'.format(job.get_id()))
			# result = word_count
		else:
			print('form is invalid')

	return render_template('home.html', form=form, result=result)


@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):

    job = Job.fetch(job_key, connection=redis_conn)
    print(job.is_finished)

    if job.is_finished:
        return str(job.result), 200
    else:
        return "Nay!", 202