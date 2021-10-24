from flask import Blueprint

bp = Blueprint('vsd', __name__)

from ..vsd import routes