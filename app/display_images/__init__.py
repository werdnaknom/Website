from flask import Blueprint

bp = Blueprint('upload', __name__)

from app.display_images import routes