from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd6ad308f0cf0e8542f894171ea38fb31'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #relative path from the current file

db = SQLAlchemy(app)  # db instance

from flaskblog import routes