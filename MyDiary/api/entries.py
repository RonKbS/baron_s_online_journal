from flask import jsonify, request
from MyDiary import model
from MyDiary.api import bp
from MyDiary.model import Diary


@bp.route('/entries/<int:entry_id>', methods=['GET'])
def get_entry(entry_id):
    if type(Diary.find_entry_by_id(entry_id)) == dict:
        return jsonify(Diary.find_entry_by_id(entry_id)), 200
    return jsonify({404: Diary.find_entry_by_id(entry_id)}), 404


@bp.route('/entries', methods=['GET'])
def get_all_entries():
    return jsonify({'Entries': Diary.list_all_entries()})


@bp.route('/entries', methods=['POST'])
def add_entry():
    new_entry = request.get_json() or {}
    Diary.add_entry(new_entry["content"])
    return jsonify({201: 'Entry added'}), 201


@bp.route('/entries/<int:entry_id>', methods=['PUT'])
def change_entry(entry_id):
    entry_change = request.get_json() or {}
    Diary.modify_entry(entry_change["content"])
    return jsonify({201: 'Entry has been modified'})


@bp.route('/entries/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    if type(Diary.find_entry_by_id(entry_id)) == dict:
        return jsonify({200: Diary.delete_entry(entry_id)}), 200
    return jsonify({404: Diary.find_entry_by_id(entry_id)}), 404
