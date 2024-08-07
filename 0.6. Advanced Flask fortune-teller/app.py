from flask import Flask, render_template
import random

app = Flask(__name__, 
	template_folder = 'templates',
	static_folder = 'static')

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


indecisive_fortunes = []


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/fortune')
def fortune():
	random_fortune = random.choice(fortunes)
	return render_template('fortune.html', fortune_=random_fortune)



@app.route('/indecisive')
def indecisive():
	for i in range(3):
		indecisive_fortune = random.choice(fortunes)
		indecisive_fortunes.append(indecisive_fortune)
	return render_template('indecisive.html', indecisive_fortune1 = indecisive_fortunes)



if __name__ == '__main__':
    app.run(debug=True)