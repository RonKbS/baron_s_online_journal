from flask import Flask
from testing_database.create_tables import create_tables
from config import Config
import os

app = Flask(__name__)
app.config['TESTING'] = False
# app.config['SECRET_KEY'] = "\xb78\xd1\xd6\xff\x94IF\xbao\x13\xa8\x11\x94\xe0\x8d\xf3aU\xf7\xceK<\x97<x97"
# create_tables('users' , 'entries')
Config.db

from mydiary.api import bp as bp_api
app.register_blueprint(bp_api, url_prefix='/api/v1')

#from MyDiary import routes