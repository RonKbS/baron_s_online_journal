from flask import Blueprint


bp = Blueprint('api', __name__)

from mydiary.api import entries