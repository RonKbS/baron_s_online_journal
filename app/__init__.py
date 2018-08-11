import os
import psycopg2
from flask import Flask
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
app.config['TESTING'] = False
app.config['connection'] = psycopg2.connect(
            database='travis_ci_test',
            user='postgres',
            password=' ',
            host='localhost',
            port='5432')
from database.queries import db
datab = db()
datab.create_tables('users', 'entries')

from app.api import bp as bp_api
app.register_blueprint(bp_api, url_prefix='/api/v1')
