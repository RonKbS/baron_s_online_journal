from flask import Flask
from flask_login import LoginManager


app = Flask(__name__)
login = LoginManager(app)
login.login_view = 'login'

from mydiary.api import bp as bp_api
app.register_blueprint(bp_api, url_prefix='/api/v1')
