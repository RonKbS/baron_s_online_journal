from flask import g
from flask_httpauth import HTTPBasicAuth
from mydiary.model import Diary
from flask_httpauth import HTTPTokenAuth

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verify_password(username, password):
    for user in Diary.users:
        if user['name'] == username:
            '''save authenticated user in loacal proxy g
            to be accessible from API functions'''
            g.current_user = user
            return Diary.check_password(password)
    return False

@token_auth.verify_token
def verify_token(token):
    g.current_user = Diary.check_token(token) if token else None
    return g.current_user is not None
