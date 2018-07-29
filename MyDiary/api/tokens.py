from flask import jsonify, g
from MyDiary.api import bp
from MyDiary.api.authentication import basic_auth

@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_toke():
    token = g.current_user.get_token()
    return jsonify({'token': token})
