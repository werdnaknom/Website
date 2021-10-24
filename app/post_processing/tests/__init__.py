from flask import Blueprint

bp = Blueprint('postprocessing', __name__)

from ..tests import post_processing_routes