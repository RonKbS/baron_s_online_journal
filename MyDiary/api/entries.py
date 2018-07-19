from flask import jsonify, request
from mydiary import model
from mydiary.api import bp
from mydiary.model import Diary


@bp.route('/entries/<string:date>', methods=['GET'])
def get_entry(date):
    if type(Diary.find_entry_by_date(date)) == dict:
        return jsonify(Diary.find_entry_by_date(date)), 200
    return jsonify({404: Diary.find_entry_by_date(date)})


@bp.route('/entries', methods=['GET'])
def get_all_entries():
    return jsonify({'Entries': Diary.list_all_entries()})


@bp.route('/entries', methods=['POST'])
def add_entry(date):
    new_entry = request.get_json() or {}
    Diary.add_entry(new_entry)
    return jsonify({201: 'Entry added'})
