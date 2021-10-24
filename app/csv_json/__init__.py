from flask import Blueprint

bp = Blueprint('csv', __name__)

from app.csv_json import routes