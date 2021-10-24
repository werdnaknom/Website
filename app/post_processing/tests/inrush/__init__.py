from flask import Blueprint

bp = Blueprint('inrush', __name__)

from ..inrush import routes