from flask import Blueprint

bp = Blueprint('edge_power', __name__)

from ..edge_power import routes