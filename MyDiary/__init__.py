from flask import Flask

app = Flask(__name__)

from MyDiary.api import bp as bp_api
app.register_blueprint(bp_api, url_prefix='/api/v1')

#from MyDiary import routes