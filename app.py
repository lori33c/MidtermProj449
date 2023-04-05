from flask import Flask
import pymysql
from flask_cors import CORS

app = Flask(__name__)

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
    return "Hello, Flask!"