from flask import Flask, render_template, request, redirect, url_for
from flask import session as login_session
import pyrebase

app = Flask(__name__, 
	template_folder = 'templates',
	static_folder = 'static')
app.config['SECRET_KEY'] = '*******'


firebaseConfig = {
  "apiKey" : "AIzaSyBIFULHu9GT1rXfUWSUfbK0HkVB2MjbEdU",
  "authDomain" : "authenticationlab-f6a8d.firebaseapp.com",
  "projectId" : "authenticationlab-f6a8d",
  "storageBucket": "authenticationlab-f6a8d.appspot.com",
  "messagingSenderId": "853516923794",
  "appId": "1:853516923794:web:9eddd319f04cb1d938874b",
  "measurementId": "G-F5T6S19W86",
  "databaseURL":"https://authenticationlab-f6a8d-default-rtdb.europe-west1.firebasedatabase.app/"
}


firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()



@app.route('/home', methods = ['POST', 'GET'])
def home():
	if request.method == 'GET':
		return render_template("home.html")
	else:
		quotes = []
		quote = request.form['quote']
		quoter = request.form['quoter']
		if quote and quoter:
			quotes.append(quote)
			login_session['qoutes'] = quotes
			login_session.modified = True
			quotes1 = login_session['qoutes']
			user_id = login_session['users']['localId']
			quoteees = {"Quote" : quotes1, "Sayer": quoter, "uid": user_id}
			db.child("Quotes").push(quoteees)
			return redirect(url_for('thanks'))



@app.route('/', methods = ['POST', 'GET'])
def signup():
	if request.method == 'GET':
		return render_template("signup.html")
	else:
		email = request.form['email']
		password = request.form['password']
		fullname = request.form['fullname']
		username = request.form['username']
		try:
			login_session['users'] = auth.create_user_with_email_and_password(email, password)
			user_id = login_session['users']['localId']
			db.child("users").child(user_id).set({
			"fullname": fullname,
			"username": username 
			})
			return redirect('home')
		except Exception as a:
			print(a)
			error = "failed"
			return render_template("signup.html")


@app.route('/signin', methods = ['POST', 'GET'])
def signin():
	if request.method == 'GET':
		return render_template("signin.html")
	else:

		email = request.form['email']
		password = request.form['password']

		try:

			login_session['user'] = auth.sign_in_with_email_and_password(email, password)
			return redirect(url_for('home'))
		
		except:
			error = "failed"
			print(error)
			return render_template("signin.html")

	



@app.route('/signout', methods = ['POST', 'GET'])
def signout():
	auth.current_user = None
	return render_template('signin.html')


@app.route('/display', methods = ['POST', 'GET'])
def display():
	quote = db.child("Quotes").child("Qoute").get().val()
	sayer = db.child("Quotes").child("Sayer").get().val()
	quotes2 = []
	quotes2.append(quote)
	quotes2.append(sayer)
	return render_template("display.html", quotes = quotes2)


@app.route('/thanks', methods = ['POST', 'GET'])
def thanks():
	return render_template("thanks.html")


if __name__ == "__main__":
	app.run(debug=True)