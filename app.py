import requests
from flask import Flask, render_template, redirect, url_for, request
from forms import UrlInputForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f97d8be751f31b5f16f143bb9fef833e'



def count_words_at_url(url):
	resp = requests.get(url)
	return len(resp.text.split())



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