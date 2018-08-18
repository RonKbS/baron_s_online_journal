import jwt
import datetime
from pyisemail import is_email
from config import Config
from flask import jsonify, request, make_response, redirect
from app import model
from app.api import bp
from app.model import Users, Diary
from functools import wraps
from database.queries import db


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'token' in request.headers:
            token = request.headers['token']
        elif not token:
            return jsonify({'token': 'Token is missing'}), 401
        try:
            user_id = jwt.decode(token, Config.SECRET_KEY)
            current_user = db.find_user_by_id(user_id['id'])
        except BaseException:
            #import pdb; pdb.set_trace()
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user['user_id'], *args, **kwargs)
    return decorated


@bp.route('/docs')
def docs():
    return redirect('https://baronsmydiary.docs.apiary.io/')


@bp.route('/login', methods=['POST'])
def login():
    try:
        auth = request.get_json() or {}

        logged_user = db.find_user_by_name(auth['name'])

        if not logged_user:
            return jsonify({'Message': 'Wrong credentials entered'}), 400

        if Users.check_password(logged_user['password'], auth['password']):
            token = jwt.encode({'id': logged_user['user_id'],
                                'exp': datetime.datetime.utcnow() +
                                datetime.timedelta(minutes=30)}, Config.SECRET_KEY)
            return jsonify({'token': token.decode('UTF-8')})
        return jsonify({'Message': 'Wrong credentials entered'}), 400
    except BaseException:
        return jsonify({'Message': 'Wrong format used'}), 400


@bp.route('/auth/signup', methods=['POST'])
def add_user():
    try:
        user = request.get_json() or {}

        if (db.reg_ex(user['name']) == False\
        or db.reg_ex(user['password']) == False) or\
        (len(user['name']) and len(user['password'])) < 5:
            return jsonify(
                {'Message': 'Password and username should be atleast 5 alphanumeric characters and contain no spaces'}), 400

        if not is_email(user['email']):
            return jsonify({'Message': 'Wrong email, format'}), 400

        if not db.find_user_by_name(user['name']):
            Users.add_user(
                user['name'],
                user['email'],
                Diary.set_password(
                    user['password']))
            return jsonify({'Message': "Karibu! Let's begin by logging in"}), 201
        return jsonify({'Message': 'User exists'}), 400
    except BaseException:
        return jsonify({'Message': 'Wrong format used'}), 400


@bp.route('/account', methods=['PUT'])
@token_required
def update(user_id):
    try:
        details = request.get_json() or {}
        if is_email(details['email']):
            Users.modify_detail(user_id, details['email'])
            return jsonify({"Message": 'Email has been changed'}), 201
        elif db.reg_ex(details['password']) and len(details['password']) > 5:
            Users.modify_detail(user_id, details['email'])
            return jsonify({"Message": 'Password has been changed'}), 201
        return jsonify({'Message': 'Details incorrectly worded'})
    except BaseException:
        return jsonify({'Error': 'Wrong format used'}), 400


@bp.route('/entries/<int:entry_id>', methods=['GET'])
@token_required
def get_entry(user_id, entry_id):
    if Diary.find_entry_by_id(user_id, entry_id) != 'No such entry':
        return jsonify(Diary.find_entry_by_id(user_id, entry_id)), 200
    return jsonify({"Error": Diary.find_entry_by_id(user_id, entry_id)}), 404


@bp.route('/entries', methods=['GET'])
@token_required
def get_all_entries(user_id):
    return jsonify({'Entries': Diary.list_all_entries(user_id)})


@bp.route('/entries', methods=['POST'])
@token_required
def add_entry(user_id):
    '''Obtain the entry sent as a dictionary then append it_to entries list'''
    new_entry = request.get_json() or {}
    if new_entry:
        Diary.add_entry(new_entry["title"], new_entry["content"], user_id)
        return jsonify({"Message": 'Entry added'}), 201
    else:
        jsonify({'Error': 'Wrong format used to send data'}), 400


@bp.route('/entries/<int:entry_id>', methods=['PUT'])
@token_required
def change_entry(user_id, entry_id):
    new_entry = request.get_json() or {}
    if Diary.modify_entry(
            user_id,
            entry_id,
            new_entry['title'],
            new_entry['content']) == 'No such entry':
        return jsonify({"Error": 'No such entry'}), 200
    Diary.modify_entry(
        user_id,
        entry_id,
        new_entry['title'],
        new_entry['content'])
    return jsonify({"Message": 'Entry has been modified'}), 201


@bp.route('/entries/<int:entry_id>', methods=['DELETE'])
@token_required
def delete_entry(user_id, entry_id):
    if Diary.delete_entry(user_id, entry_id) == 'Entry deleted':
        return jsonify({"Message": 'Entry deleted'}), 200
    return jsonify({"Error": Diary.find_entry_by_id(user_id, entry_id)}), 404
