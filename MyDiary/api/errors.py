from flask impoer jsonify
from werkzeug.http import HTTP_STATUS_CODES


def response_to_error(status_code):
    payload {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    response = jsonify(payload) #set status_code after creating response
    response.status_code = status_code #code is set to correct one bcoz jsonify returns default 200
    return response