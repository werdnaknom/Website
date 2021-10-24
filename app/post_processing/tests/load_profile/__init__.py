from flask import Blueprint

bp = Blueprint('load_profile', __name__)

from ..load_profile import routes