import os
import psycopg2
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    '''Generated from print(uuid.uuid4().hex)'''
    '''Create tables, automatically if on local'''
    connection = psycopg2.connect(
            database='travis_ci_test',
            user='postgres',
            password=' ',
            host='localhost',
            port='5432')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'try_and_guess'

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['send@from_this_email.com']
