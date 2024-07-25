from flask import Flask, render_template, request, redirect, url_for
from flask import session as login_session
import random
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


pop = ["The Rise and Fall of a Midwest Princess - Chappell Roan",
	  "Isolation - Kali Uchis",
	  "ArtPop - Ladygaga", 
	  "Future Nostalgia - Dua Lipa",
    "Chromatica - Lady Gaga",
    "Fine Line - Harry Styles",
    "Positions - Ariana Grande",
    "After Hours - The Weeknd",
    "Folklore - Taylor Swift",
    "When We All Fall Asleep, Where Do We Go? - Billie Eilish",
    "Rare - Selena Gomez",
    "Lover - Taylor Swift",
    "thank u, next - Ariana Grande"]

indie = ["The Land is Inhospitable and so are we - Mitski",
 "The Bends - Radiohead", "OK computer - Radiohead",
  "Lush - Mitski",
  "Stranger in the Alps - Phoebe Bridgers",
  "Currents - Tame Impala",
  "Punisher - Phoebe Bridgers",
  "An Awesome Wave - alt-J",
  "The New Abnormal - The Strokes",
  "I Like It When You Sleep, for You Are So Beautiful yet So Unaware of It - The 1975",
  "How Big, How Blue, How Beautiful - Florence + The Machine",
  "Bury Me at Makeout Creek - Mitski",
  "Violet Street - Local Natives",
  "Shore - Fleet Foxes"]

rock = ["The Dark side of the moon - Pink Floyd", 
		"Rainbows - Radiohead", 
		"Back In Black - AC/DC", "Led Zeppelin IV - Led Zeppelin",
    "Abbey Road - The Beatles",
    "Dark Side of the Moon - Pink Floyd",
    "Back in Black - AC/DC",
    "Hotel California - Eagles",
    "Appetite for Destruction - Guns N' Roses",
    "Rumours - Fleetwood Mac",
    "The Wall - Pink Floyd",
    "Born to Run - Bruce Springsteen"]

jazz = ["The World We Knew - Frank Sinatra", 
		"Bewitched - laufey", 
		"Love Deluxe - sade", 
		"Solitude - Billie Holiday",
		"Kind of Blue - Miles Davis",
    "A Love Supreme - John Coltrane",
    "Time Out - The Dave Brubeck Quartet",
    "Blue Train - John Coltrane",
    "Mingus Ah Um - Charles Mingus",
    "Head Hunters - Herbie Hancock",
    "Somethin' Else - Cannonball Adderley",
    "Speak No Evil - Wayne Shorter",
    "Maiden Voyage - Herbie Hancock"]


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
			"username": username, 
			},
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
	if request.method == 'GET':
		return render_template("home.html")
	else:
		try: 
			cleangenre = request.form['genrecl']
			studygenre = request.form['genrest']
			shopgenre = request.form['genresh']
			meditategenre = request.form['genreme']
			othergenre = request.form['genreot']

			mazika = {"Cleaning" : cleangenre, "Studying" : studygenre, "Shopping" : shopgenre, "Meditating" : meditategenre, "Other" : othergenre}

			for key in mazika.keys():
				if mazika[key] == "pop":
					mazika[key] = random.choice(pop)
				elif key == "indie":
					mazika[key] = random.choice(indie)
				elif key == "rock":
					mazika[key] = random.choice(rock)
				else:
					mazika[key] = random.choice(jazz)
			print(mazika)

			db.child('users').child(login_session['users']['localId']).child('user_info').child('mazika').set(mazika)

			return redirect('/list')

		except:

			error = "failed"
			print(error)
			return render_template("home.html")



@app.route('/list', methods = ['POST', 'GET'])
def list():
	if request.method == 'GET':
		return render_template("list.html", tasks = db.child('users').child(login_session['users']['localId']).child('todo').child('tasks').child('cats').get().val(),genres = db.child('users').child(login_session['users']['localId']).child('user_info').child('mazika').get().val())
	
	else:
		try: 
			task = request.form['task']
			category = request.form['cat']


			db.child('users').child(login_session['users']['localId']).child('todo').child('tasks').child(underscore(task)).set({
				"name": task,
				"category": category
				})


			tasks1 = db.child('users').child(login_session['users']['localId']).child('todo').child('tasks').get().val()

			print(f"printing tasks: {tasks1}")

			return render_template("list.html", tasks = tasks1, genres = db.child('users').child(login_session['users']['localId']).child('user_info').child('mazika').get().val())

		except Exception as a:

			print(a)
			return render_template("list.html", tasks = db.child('users').child(login_session['users']['localId']).child('todo').child('tasks').child('cats').get().val(), genres = db.child('users').child(login_session['users']['localId']).child('user_info').child('mazika').get().val())


@app.route('/clear_tasks', methods = ['POST', 'GET'])
def clear():
	db.child('users').child(login_session['users']['localId']).child('todo').child('tasks').remove()
	return render_template("list.html", tasks=None, genres = db.child('users').child(login_session['users']['localId']).child('user_info').child('mazika').get().val())


@app.route('/deletetask', methods = ['POST', 'GET'])
def delete():
	print(f"hi sisters: {request.form.to_dict()}")

	if request.method == 'POST':

		delete = request.form.get('task1')
		db.child('users').child(login_session['users']['localId']).child('todo').child('tasks').child(delete).remove()
	
		return render_template('list.html', tasks =db.child('users').child(login_session['users']['localId']).child('todo').child('tasks').get().val(), genres = db.child('users').child(login_session['users']['localId']).child('user_info').child('mazika').get().val())


def underscore(keytask):
	s1 = " "
	s2 = "_"
	input_string = keytask.replace(s1, s2)
	return input_string

if __name__ == "__main__":
	app.run(debug=True)
 	