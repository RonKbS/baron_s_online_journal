from flask import Flask
from config import Config


app = Flask(__name__)
'''This next line tells Flask to read and apply config file'''
app.config.from_object(Config)


from mydiary.api import bp as bp_api
app.register_blueprint(bp_api, url_prefix='/api/v1')
