from flask import jsonify, request, make_response
from mydiary import model
from mydiary.api import bp
from mydiary.model import Diary, Users
from flask_login import login_required
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from config import Config
import datetime
from functools import wraps



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        elif not token:
            return jsonify({'token': 'token is missing'})
        try:
            data = jwt.decode(token, Config.SECRET_KEY)
            for user in Users.users:
                if user['name'] == data['name']:
                    current_user = user
                    break
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@bp.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.name or not auth.password:
        return make_response('Could not verify', 401, 
                            {'WWW-Authenticate': 'Basic Realm = "Login Required"'})
    for user in Users.users:
        if user['name'] == auth.name:
            logged_user = user
            break
    if not logged_user:
        return make_response('Could not verify', 401, 
                            {'WWW-Authenticate': 'Basic Realm = "Login Required"'})

    if check_password_hash(user['password'], auth.password):
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow() +
                             datetime.timedelta(minutes=(1))}, Config.SECRET_KEY)
        return jsonify({'token': token.decode('UTF-8')})
    token = jwt.encode({'password': logged_user['password'], 'exp': datetime.datetime.utcnow()
                            + datetime.timedelta(minutes=(1))}, Config.SECRET_KEY)

@bp.route('/entries/<int:entry_id>', methods=['GET'])
@token_required
def get_entry(entry_id):
    if type(Diary.find_entry_by_id(entry_id)) == dict:
        return jsonify(Diary.find_entry_by_id(entry_id)), 200
    return jsonify({404: Diary.find_entry_by_id(entry_id)}), 404


@bp.route('/entries', methods=['GET'])
@token_required
def get_all_entries(user_id):
    return jsonify({'Entries': Diary.list_all_entries()})


@bp.route('/entries', methods=['POST'])
@token_required
def add_entry():
    '''Obtain the entry sent as a dictionary then append it to entries list'''
    new_entry = request.get_json() or {}
    new_entry_return = Diary.add_entry(new_entry["content"])
    if new_entry_return == "New entry is similar to older entry":
        return jsonify({403 : new_entry_return}), 403
    return jsonify({201: 'Entry added'}), 201


@bp.route('/entries/<int:entry_id>', methods=['PUT'])
@token_required
def change_entry(user_id, entry_id):
    new_entry = request.get_json() or {}
    if Diary.modify_entry(user_id, entry_id, new_entry['content']) == 'No such entry':
        return jsonify({404: 'No such entry'}), 404
    Diary.modify_entry(user_id, entry_id, new_entry['content'])
    return jsonify({201: 'Entry has been modified'}), 201


@bp.route('/entries/<int:entry_id>', methods=['DELETE'])
@token_required
def delete_entry(user_id, entry_id):
    if type(Diary.find_entry_by_id(user_id, entry_id)) == dict:
        return jsonify({200: Diary.delete_entry(entry_id)}), 200
    return jsonify({404: Diary.find_entry_by_id(entry_id)}), 404
