import os
import atexit
import psycopg2
from flask import Flask
from config import Config
from flask_mail import Mail
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)
app.config.from_object(Config)
app.config['TESTING'] = False
app.config['connection'] = psycopg2.connect(
            database='users',
            user='postgres',
            password=' ',
            host='localhost',
            port='5432')
mail = Mail(app)


from database.queries import db
datab = db()
datab.create_tables('users', 'entries', 'notifications')


scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=datab.send_email,
    trigger=IntervalTrigger(minutes=0.5),
    id='sending_mails',
    name='Send email notifications daily',
    replace_existing=True
)
atexit.register(lambda: scheduler.shutdown())

from app.api import bp as bp_api
app.register_blueprint(bp_api, url_prefix='/api/v1')
