from flask import Blueprint

bp = Blueprint('testpoints', __name__)

from app.testpoints import routes