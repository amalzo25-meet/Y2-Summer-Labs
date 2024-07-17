from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__, 
	template_folder = 'templates',
	static_folder = 'static')


@app.route('/', methods = ['POST', 'GET'])
def home():
	if request.method == 'GET':
		return render_template('home.html')
	else:
		birthday = request.form['birthday']
		return redirect(url_for('fortune', birthday=birthday))

@app.route('/fortune/<birthday>')
def fortune(birthday):
	fortunes = ["Having to eat IASA`s food for the rest of your life", 
	"Abdalla is going to chase you around IASA" , 
	"The next lab bonus you will try to complete is going to be easy", 
	"Your favorite complimentary from y1 is coming back",
	"You get home to find your favorite meal on the kitchen table",
	"You will get the 6 people room with tiny bathrooms next week",
	"You will get wide comfortable 4 people room next week",
	"You get home to find 10 million dollars on your bed",
	"Your next CS lab will be long and hard",
	"You will be famous in the future",
	"You will fall down infront of everyone in the cafeteria",
	]
	if len(birthday) < 10:
		fortune1 = fortunes[len(birthday)]
		return render_template('fortune.html', fortune_= fortune1, birthday=birthday)
	else:
		return render_template('birthdaymnth.html')


if __name__ == '__main__':
    app.run(debug=True)