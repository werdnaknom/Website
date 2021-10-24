from flask import Blueprint

bp = Blueprint('testplan', __name__)

from app.testplan import routes