import requests
from flask import Flask, render_template, redirect, url_for, request
from forms import UrlInputForm
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'f97d8be751f31b5f16f143bb9fef833e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///edyst.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Counter(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	url = db.Column(db.String, nullable=False)
	word_count = db.Column(db.Integer, nullable=False)


	def __repr__(self):
		return '{0} has {1} words'.format(self.url, self.word_count)



def count_words_at_url(url):
	resp = requests.get(url)
	word_count = len(resp.text.split())
	try:
		instance = Counter(url=url, word_count=word_count)
		db.session.add(instance)
		db.session.commit()
	except:
		print('not able to insert in db')
		
	return word_count



@app.route('/', methods=['GET', 'POST'])
def home():
	result = None
	form = UrlInputForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			word_count = count_words_at_url(form.url.data)
			result = word_count
		else:
			print('form is invalid')

	return render_template('home.html', form=form, result=result)


if __name__ == '__main__':
	app.run(debug=True)