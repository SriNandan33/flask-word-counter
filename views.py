from flask import request, render_template, redirect
from rq.job import Job
from config import app, q
from worker import conn
from forms import UrlInputForm
from models import Counter

# views

@app.route('/', methods=['GET', 'POST'])
def home():
	result = None
	form = UrlInputForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			input_url = form.url.data
			job = q.enqueue_call(
            	func='utils.count_words_at_url', args=(input_url,), result_ttl=5000
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