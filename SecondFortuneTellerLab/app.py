from flask import Flask, render_template, request, redirect, url_for
from flask import session as login_session
import random

app = Flask(__name__, 
	template_folder = 'templates',
	static_folder = 'static')
app.config['SECRET_KEY'] = "Password"



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

@app.route('/', methods = ['POST', 'GET'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	else:
		login_session["birthday"]= request.form["birthday"]
		login_session["name"]= request.form["name"]
		return redirect(url_for('home'))



@app.route('/home', methods = ['POST', 'GET'])
def home():
		return render_template('home.html', name = login_session["name"])


@app.route('/fortune')
def fortune():
	if len(login_session["birthday"]) < 10:
		fortune1 = fortunes[len(login_session["birthday"])]
		return render_template('fortune.html', fortune_= fortune1, name =login_session["name"])
	else:
		return render_template('birthdaymnth.html')


@app.route('/indecisive')
def indecisive():
	indecisive_fortunes = []
	for i in range(3):
		if len(indecisive_fortunes) >= 3:
			break		
		indecisive_fortune = random.choice(fortunes)
		indecisive_fortunes.append(indecisive_fortune)

	return render_template('indecisive.html', indecisive_fortune1 = indecisive_fortunes)



if __name__ == '__main__':
    app.run(debug=True)