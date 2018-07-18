from flask import Blueprint as bp, jsonify
from MyDiary.model import Diary

@bp.route('/entries/<str:date>', methods=['GET'])
def get_entry(date):
    if type(Diary.find_entry_by_date(date)) == dict:
        return jsonify(Diary.find_entry_by_date(date)), 200
    return jsonify({404: Diary.find_entry_by_date(date)})