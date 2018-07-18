from flask import jsonify
from MyDiary.api import bp
from MyDiary.model import Diary

@bp.route('/entries/<string:date>', methods=['GET'])
def get_entry(date):
    if type(Diary.find_entry_by_date(date)) == dict:
        return jsonify(Diary.find_entry_by_date(date)), 200
    return jsonify({404: Diary.find_entry_by_date(date)})