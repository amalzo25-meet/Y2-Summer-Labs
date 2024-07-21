from flask import Flask, render_template, request, redirect, url_for
from flask import session as login_session
import pyrebase

app = Flask(__name__, 
	template_folder = 'templates',
	static_folder = 'static')
app.config['SECRET_KEY'] = 'super-secret-key'


firebaseConfig = {
  "apiKey" : "AIzaSyBIFULHu9GT1rXfUWSUfbK0HkVB2MjbEdU",
  "authDomain" : "authenticationlab-f6a8d.firebaseapp.com",
  "projectId" : "authenticationlab-f6a8d",
  "storageBucket": "authenticationlab-f6a8d.appspot.com",
  "messagingSenderId": "853516923794",
  "appId": "1:853516923794:web:9eddd319f04cb1d938874b",
  "measurementId": "G-F5T6S19W86"
}


firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()


@app.route('/', methods = ['POST', 'GET'])
def signup():
	if request.method == 'GET':
		return render_template("signup.html")
	else:
		login_session['user']['email'] = request.form['email']
		login_session['user']['password'] = request.form['password']
		return redirect(url_for('home'))


@app.route('/signin', methods = ['POST', 'GET'])
def signin():
	if request.method == 'GET':
		return render_template("signin.html")
	else:
		login_session['user']['email'] = request.form['email']
		login_session['user']['password'] = request.form['password']
		login_session['user']['qoutes'] = []
		return redirect(url_for('home'))
	


@app.route('/home', methods = ['POST', 'GET'])
def home():
	return render_template("home.html")


@app.route('/signout', methods = ['POST', 'GET'])
def signout():
	return render_template('signin')


@app.route('/display', methods = ['POST', 'GET'])
def display():
	return render_template("display.html")


@app.route('/thanks', methods = ['POST', 'GET'])
def thanks():
	render_template("thanks.html")


if __name__ == "__main__":
	app.run(debug=True)