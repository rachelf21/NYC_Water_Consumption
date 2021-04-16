from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from sqlalchemy import create_engine
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

login_manager = LoginManager(app)
login_manager.login_view = "login"  #value is function for login, same as url_for
login_manager.login_message_category = 'info'

DB_URL = os.environ['NYC_WATER_DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

db = SQLAlchemy(app)
engine = create_engine(DB_URL)

from app import routes