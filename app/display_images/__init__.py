from flask import Blueprint

bp = Blueprint('display', __name__)

from app.display_images import routes
