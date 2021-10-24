from flask import Blueprint

bp = Blueprint('tasks', __name__)

from ..task_pages import task_routes