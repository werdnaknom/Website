from . import bp as bp

from flask import render_template

from ..test_route_builder import build_test_route


@bp.route('/start', methods=['GET', 'POST'])
def start():
    page = build_test_route(test_name="sequencing")
    return render_template('test_outputs/test_output.html', page=page)