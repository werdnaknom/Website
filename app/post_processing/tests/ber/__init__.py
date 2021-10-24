from flask import Blueprint

bp = Blueprint('ber', __name__)

from ..ber import routes