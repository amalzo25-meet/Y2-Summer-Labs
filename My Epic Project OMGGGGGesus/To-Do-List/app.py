from flask import Flask, render_template, request, redirect, url_for
from flask import session as login_session
import pyrebase

app = Flask(__name__, 
	template_folder = 'templates',
	static_folder = 'static')
app.config['SECRET_KEY'] = '*******'


firebaseConfig = {
  "apiKey": "AIzaSyBn6gs-fOCaFwXME6dFc-klPqIqMadv5V0",
  "authDomain": "personalproject-cd83f.firebaseapp.com",
  "databaseURL": "https://personalproject-cd83f-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "personalproject-cd83f",
  "storageBucket": "personalproject-cd83f.appspot.com",
  "messagingSenderId": "566269582330",
  "appId": "1:566269582330:web:8218486e6f271c0ac26243",
  "measurementId": "G-QZLHN106DK"}



firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()


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
			"user_info" :  {
			"fullname": fullname,
			"username": username },
			"todo" : {"tasks": []}
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


@app.route('/home', methods = ['POST', 'GET'])
def home():
	return render_template("home.html")


@app.route('/list', methods = ['POST', 'GET'])
def list():
	if request.method == 'GET':
		return render_template("list.html", tasks = db.child('users').child(login_session['users']['localId']).child('todo').child('tasks').get().val())
	else:
		task = request.form['task']
		try:
			db.child('users').child(login_session['users']['localId']).child('todo').child('tasks').child(underscore(task)).set(task)
			tasks1 = db.child('users').child(login_session['users']['localId']).child('todo').child('tasks').get().val()
			print(f"printing tasks: {tasks1}")
			return render_template("list.html", tasks = tasks1)

		except Exception as a:
			print(a)
			return render_template("list.html")

@app.route('/clear_tasks', methods = ['POST', 'GET'])
def clear():
	db.child('users').child(login_session['users']['localId']).child('todo').child('tasks').remove()
	return render_template("list.html", tasks=None)



@app.route('/deletetask', methods = ['POST', 'GET'])
def delete():
	print(f"hi sisters: {request.form.to_dict()}")
	if request.method == 'POST':
		print(f"this is the checkbox value{request.form.get('task1')}")
		request.form.get('task1')
		db.child('users').child(login_session['users']['localId']).child('todo').child('tasks').child(underscore(request.form.get('task1'))).remove()
		return render_template('list.html', tasks =db.child('users').child(login_session['users']['localId']).child('todo').child('tasks').get().val())


def underscore(keytask):
	s1 = " "
	s2 = "_"
	input_string = keytask.replace(s1, s2)
	return input_string

if __name__ == "__main__":
	app.run(debug=True)
 	