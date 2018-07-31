import jwt
import datetime
from config import Config
from flask import jsonify, request, make_response
from mydiary import model
from mydiary.api import bp
from mydiary.model import Users, Diary
from functools import wraps
from testing_database.find_edit import find_user_by_name, find_user_by_id

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        elif not token:
            return jsonify({'token': 'token is missing'})
        try:
            user_id = jwt.decode(token, Config.SECRET_KEY)
            current_user = find_user_by_id(user_id['id'])
        except:
            #import pdb; pdb.set_trace()
            return jsonify({'message' : 'Token is invalid!'}), 401
        return f(current_user['user_id'], *args, **kwargs)
    return decorated


@bp.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, 
                            {'WWW-Authenticate': 'Basic Realm = "Login Required"'})
    logged_user = find_user_by_name(auth.username)
        # elif not logged_user:
        #     return make_response('No such user', 401, 
        #                     {'WWW-Authenticate': 'Basic Realm = "Login Required"'})

    #import pdb; pdb.set_trace()
    if Users.check_password(logged_user['password'], auth.password):
        token = jwt.encode({'id': logged_user['user_id'], 'exp': datetime.datetime.utcnow() +
                             datetime.timedelta(minutes=30)}, Config.SECRET_KEY)
        return jsonify({'token': token.decode('UTF-8')})
    return make_response('No such user', 401, 
                        {'WWW-Authenticate': 'Basic Realm = "Login Required"'})


@bp.route('/auth/signup', methods=['POST'])
def add_user():
    user = request.get_json() or {}
    Users.add_user(user['name'], user['email'], Diary.set_password(user['password']))
    return jsonify({201: 'User added'}), 201


# @bp.route('/login')
# def login():
    
#     return make_response('Unable to verify', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

@bp.route('/entries/<int:entry_id>', methods=['GET'])
@token_required
def get_entry(user_id, entry_id):
    if Diary.find_entry_by_id(user_id, entry_id):
        return jsonify(Diary.find_entry_by_id(user_id, entry_id)), 200
    return jsonify({404: Diary.find_entry_by_id(user_id, entry_id)}), 404


@bp.route('/entries/<int:user_id>', methods=['GET'])
def get_all_entries(user_id):
    return jsonify({'Entries': Diary.list_all_entries(user_id)})


@bp.route('/entries', methods=['POST'])
@token_required
def add_entry(user_id):
    '''Obtain the entry sent as a dictionary then append it_to entries list'''
    new_entry = request.get_json() or {}
    new_entry_return = Diary.add_entry(new_entry["content"], user_id)
    if new_entry_return == "New entry is similar to older entry":
        return jsonify({403 : new_entry_return}), 403
    return jsonify({201: 'Entry added'}), 201


@bp.route('/entries/<int:entry_id>', methods=['PUT'])
def change_entry(entry_id):
    new_entry = request.get_json() or {}
    if Diary.modify_entry(entry_id, new_entry['content']) == 'No such entry':
        return jsonify({404: 'No such entry'}), 404
    Diary.modify_entry(entry_id, new_entry['content'])
    return jsonify({201: 'Entry has been modified'}), 201


@bp.route('/entries/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    if type(Diary.find_entry_by_id(entry_id)) == dict:
        return jsonify({200: Diary.delete_entry(entry_id)}), 200
    return jsonify({404: Diary.find_entry_by_id(entry_id)}), 404
