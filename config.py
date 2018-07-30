import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    '''Generated from print(uuid.uuid4().hex)'''
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'try_and_guess'

    # DATABASE_URI = os.environ.get('DATABASE_URL') or config()