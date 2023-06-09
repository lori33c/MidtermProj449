# MidtermProj449

# Contributors 
...
...
Julian Ogata
Angel Armendariz
Lori Cha

# My Flask Application
This is a Flask web application that provides user registration, login, file uploading, and viewing public information. The application uses a MySQL database for storing user information and a local folder for storing uploaded files.

# Prerequisites
Python 3.6 or later installed
MySQL Server installed and running
Virtual environment (optional but recommended)
Setup
Clone the repository or download the source code.

(Optional) Create a virtual environment:
python3 -m venv venv


# Virtual Environment/Install
Activate the virtual environment:
On Linux/macOS:
source venv/bin/activate

On Windows:
venv\Scripts\activate.bat

Install the required Python packages:
pip install -r requirements.txt


# Database Setup
## Set up the required database:
Create a database and schema in MySQL workbench with host='localhost' and user='root' with password='Password123!' and the name '449_db'
Run the python file dbschema.py

## Running the Application
Start the Flask application:
flask run 
Open your web browser and navigate to http://localhost:5000.

You should now see the home page of the Flask application. You can register, log in, upload files, and view public information.
You can only view the protected information once you are logged in 

# Database Info
The Databaase contains table(s):
* accounts

Database stores user data and login information.
You may check out the database by using MySQL Workbench or any other database manager

## MySQL Workbench
Open application
Add database w/:
* Connection Name: 449_db
* Connection Method: Standard (TCP/IP)
* Hostname: 127.0.0.1
* Port: 3306
* Username: root
* Password: Password123!

Connect!


