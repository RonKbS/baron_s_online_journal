from flask import Blueprint


bp = Blueprint('api', __name__)

from MyDiary.api import entries