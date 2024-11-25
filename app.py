from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from accidents import Accidents
from flask import jsonify
import json

app = Flask(__name__)


app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'chartdata'

mysql = MySQL(app)

@app.route('/', methods =['GET', 'POST']) 
def login():
	msg = ''
	if request.method == 'POST' and 'loginUsername' in request.form and 'loginPassword' in request.form:
		username = request.form['loginUsername']
		password = request.form['loginPassword']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM account WHERE username = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			msg = 'Logged in successfully !'
			return render_template('index.html', msg = msg)
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('username', None)
	session.pop('password', None)
	return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'signUpUsername' in request.form and 'signUpPassword' in request.form and 'signUpEmail' in request.form :
		username = request.form['signUpUsername']
		password = request.form['signUpPassword']
		email = request.form['signUpEmail']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM account  WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers !'
		elif not username or not password or not email:
			msg = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO account  VALUES (null, % s, % s, % s)', (username, email, password, ))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)


@app.route('/home')
def home():
	cursor = mysql.connection.cursor()
	cursor.execute('select population from chart_representation')
	population = cursor.fetchall()

	cursor = mysql.connection.cursor()
	cursor.execute('select year from chart_representation')
	years = cursor.fetchall()
	
	india = Accidents('India', [222840,394000,407497,406726,429910,460920,470920,523000,484704,461312,497686,490383,461312,489400,464674,464910,470403,449002,366138,412432,461312,463000,461312])
	maharashta = Accidents('Maharashtra', [5916,7941,9742,9851,7490,10282,8121,6885,3726,4243,1050,3099,3473,7121,2885,3326,4243,950,2099,1473,1232,2312,999])
	delhi = Accidents('Delhi', [11744,30000,16005,19771,20185,24377,12232,34222,23232,19800,20300,23000,34567,12345,54321,23412,32147,30912,29243,29213,25663,28978,30618])
	
	json_data = [india, maharashta, delhi] 
  
	print(json_data)

	return render_template('home.html', value=json_data)

@app.route('/charts')
def charts():
	return render_template('charts.html')

@app.route('/tutorials')
def tutorials():
	cursor = mysql.connection.cursor()
	cursor.execute('select population from chart_representation')
	population = cursor.fetchall()

	cursor = mysql.connection.cursor()
	cursor.execute('select year from chart_representation')
	years = cursor.fetchall()
	
	return render_template('tutorials.html', value=population, valueOne=years)

@app.route('/contact')
def contact():
	cursor = mysql.connection.cursor()
	cursor.execute('select accident_per_year from accident_per_year')
	accident_per_year = cursor.fetchall()

	cursor = mysql.connection.cursor()
	cursor.execute('select year from accident_per_year')
	year = cursor.fetchall()
	
	return render_template('contact.html', value=accident_per_year, valueOne=year)

@app.route('/accident')
def accident():
	return render_template('accident.html')

@app.route('/home2')
def home2():
	return render_template('home2.html')

@app.route('/population')
def population():
	return render_template('population.html')

@app.route('/accidents')
def accidents():
	cursor = mysql.connection.cursor()
	cursor.execute('select number_of_accidents from india_accident')
	accidents = cursor.fetchall()
	
	# print ("accidents", accidents)
	
	mylist=[]
	
	for accident in accidents:
		# print(accident[0])
		mylist.append(accident[0])

	# print("output:",mylist)
	# results = [tuple(row) for row in accidents]


	# print("output",results)

	# print(f"{type(results)} of type {type(results[0])}")

	json_string = json.dumps(mylist)

	print("output",json_string)

	# json_data=jsonify(accidents)
	# print("output",json_data)
	return render_template('accidents.html')


@app.route('/combined')
def combined():
	return render_template('combined.html')

@app.route('/indexhighcharts')
def indexhighcharts():
	return render_template('indexhighcharts.html')

@app.route('/explore')
def explore():
	return render_template('explore.html')

@app.route('/transport')
def transport():
	return render_template('transport.html')


@app.route('/health')
def health():
	return render_template('health.html')

@app.route('/movie')
def movie():
	return render_template('movie.html')


@app.route('/sports')
def sports():
	return render_template('sports.html')

@app.route('/income')
def income():
	return render_template('income.html')

@app.route('/internet')
def internet():
	return render_template('internet.html')



