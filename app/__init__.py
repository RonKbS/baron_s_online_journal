from flask import Flask
from testing_database.find_edit import db
# from testing_database.create_tables import create_tables
from config import Config
import os

app = Flask(__name__)
app.config['TESTING'] = False
datab = db()
datab.create_tables('users', 'entries')

from app.api import bp as bp_api
app.register_blueprint(bp_api, url_prefix='/api/v1')

#from MyDiary import routes