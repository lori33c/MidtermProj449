from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory
import pymysql
import re
import os
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

app.secret_key = 'happykey'
app.config['JWT_SECRET_KEY'] = 'secretMidtermKey'
jwt = JWTManager(app)

UPLOAD_FOLDER = 'templates/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Connecting to the MySQL database
conn = pymysql.connect(
    host='localhost',
    user='root',
    password= "Password123!",
    db='449_db',
    cursorclass=pymysql.cursors.DictCursor
)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST', 'GET'])
def upload_file():
	if request.method == 'POST':
		if 'file' not in request.files:
			return jsonify({"msg": "No file part"}), 400
		file = request.files['file']
		if file.filename == '':
			return jsonify({"msg": "No file selected"}), 400
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return jsonify({"msg": "File uploaded successfully"}), 200
		else:
			return jsonify({"msg": "File type not allowed"}), 400
	elif request.method == 'GET':
		return render_template('upload.html')


@app.route('/public', methods=['GET'])
def public():
    public_data = [
        {"id": 1, "name": "Item 1", "description": "This is a public item 1."},
        {"id": 2, "name": "Item 2", "description": "This is a public item 2."},
        {"id": 3, "name": "Item 3", "description": "This is a public item 3."},
    ]
    return render_template('public.html', public_data=public_data)

cur = conn.cursor()

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		with conn.cursor() as cur:
			cur.execute('SELECT * FROM accounts WHERE username = %s', (username,))
			account = cur.fetchone()
			conn.commit()

		if account and check_password_hash(account['password'], password):
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			access_token = create_access_token(identity=username)
			session['access_token'] = access_token
			msg = 'Logged in successfully !'
			response_html = f"""
			<p>Your access token is: {access_token}</p>
			<button onclick="goToProtectedEndpoint('{access_token}')">Go to protected endpoint</button>
			<button onclick="window.location.href='/'">Home</button>
			<button onclick="goToUploadEndpoint('{access_token}')">Upload Stuff</button>
			<script>
				function goToProtectedEndpoint(token) {{
					const headers = new Headers();
					headers.append('Authorization', 'Bearer ' + token);

					fetch('/protected', {{
						method: 'GET',
						headers: headers
					}})
					.then(response => {{
						if (response.ok) {{
							return response.text();
						}} else {{
							throw new Error('Error: ' + response.status);
						}}
					}})
					.then(data => {{
						document.body.innerHTML = data;
					}})
					.catch(error => {{
						console.error('Error fetching protected endpoint:', error);
					}});
				}}

				function goToUploadEndpoint(token) {{
					const headers = new Headers();
					headers.append('Authorization', 'Bearer ' + token);

					fetch('/upload', {{
						method: 'GET',
						headers: headers
					}})
					.then(response => {{
						if (response.ok) {{
							return response.text();
						}} else {{
							throw new Error('Error: ' + response.status);
						}}
					}})
					.then(data => {{
						document.body.innerHTML = data;
						document.getElementById('access_token').value = token; // Insert access token value into the hidden input field
					}})
					.catch(error => {{
						console.error('Error fetching upload endpoint:', error);
					}});
				}}

			</script>
			"""
			return response_html, 200, {'access_token': access_token}
		else:
			return jsonify({"msg": "Bad username or password"}), 401
	return render_template('login.html')

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
	return render_template('protected.html')


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
		hashed_password = generate_password_hash(password)
		email = request.form['email']
		with conn.cursor() as cur:
			cur.execute('SELECT * FROM accounts WHERE username = %s', (username,))
			account = cur.fetchone()
			conn.commit()

		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'name must contain only characters and numbers !'
		else:
			with conn.cursor() as cur:
				cur.execute('INSERT INTO accounts (username, email, password) VALUES (%s, %s, %s)', (username, email, hashed_password))
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