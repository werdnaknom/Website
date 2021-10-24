from flask import Blueprint

bp = Blueprint('post', __name__)

from ..post_processing import routes, models
