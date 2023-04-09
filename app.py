from flask import Flask, render_template, request, redirect, url_for, session
import pymysql
import re
from flask_cors import CORS

app = Flask(__name__)

app.secret_key = 'happykey'

# Connecting to the MySQL database
conn = pymysql.connect(
    host='localhost',
    user='root',
    password= "Password123!",
    db='449_db',
    cursorclass=pymysql.cursors.DictCursor
)

cur = conn.cursor()

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cur.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password))
		conn.commit()
		account = cur.fetchone()
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
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'password' in request.form:
		print('reached')
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		cur.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
		account = cur.fetchone()
		print(account)
		conn.commit()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'name must contain only characters and numbers !'
		else:
			cur.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, email, password))
			conn.commit()

			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)

@app.route('/about')
def about():
    msg = ''
    return render_template('about.html', msg = msg)

@app.errorhandler(400)
def cannotprocess(e):
    return render_template('error.html', error = 400)

@app.errorhandler(401)
def DNSissue(e):
    return render_template('error.html', error = 401)

@app.errorhandler(404)
def notfound(e):
    return render_template('error.html', error = 404)

@app.errorhandler(500)
def unexpectederror(e):
    return render_template('error.html', error = 500)



if __name__ == "__main__":
	app.run(host ="localhost", port = int("5000"))