from flask import Flask
from database.queries import db
from config import Config
import os

app = Flask(__name__)
app.config['TESTING'] = False
datab = db()
datab.create_tables('users', 'entries')

from app.api import bp as bp_api
app.register_blueprint(bp_api, url_prefix='/api/v1')
