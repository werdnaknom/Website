from flask import Blueprint

bp = Blueprint('sequencing', __name__)

from ..sequencing import routes