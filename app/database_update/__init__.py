from flask import Blueprint

bp = Blueprint('database_update', __name__)

from app.database_update import routes
