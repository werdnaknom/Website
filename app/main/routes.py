from flask import render_template
from app.main import bp

from database_functions.mongodatabase_functions import MongoDatabaseFunctions


@bp.route('/dashboard')
@bp.route('/index')
@bp.route('/')
def index():
    return render_template('main/dashboard.html', title="Dashboard")


@bp.route('/table')
def table():
    return render_template('table-filters-datatables.html')

