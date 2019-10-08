from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt # lesson 6 for hashing pwd
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd6ad308f0cf0e8542f894171ea38fb31'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #relative path from the current file

db = SQLAlchemy(app)  # db instance
bcrypt = Bcrypt(app)  # bcrypt instance for pwd hashing
login_manager = LoginManager(app) #it will handle all of the session

login_manager.login_view = 'login' # making sure user is logged in to view account setting
login_manager.login_message_category = 'info' # color message

from flaskblog import routes 

