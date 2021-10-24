from flask import Blueprint

bp = Blueprint('on_time', __name__)

from ..on_time import routes