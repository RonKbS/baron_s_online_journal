import os
from dotenv import load_dotenv
from testing_database.create_tables import create_tables

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    '''Generated from print(uuid.uuid4().hex)'''
    '''Create tables, automatically if on local'''
    db = os.environ.get('DATABASE_URL')
    create_tables('users', 'entries')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'try_and_guess'