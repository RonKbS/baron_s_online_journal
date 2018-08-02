import os
from dotenv import load_dotenv
from database.queries import db

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    '''Generated from print(uuid.uuid4().hex)'''
    '''Create tables, automatically if on local'''
    datab = db()
    datab.create_tables('users', 'entries')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'try_and_guess'