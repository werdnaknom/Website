from . import bp as ber_bp

from flask import render_template

from ..test_route_builder import build_test_route


@ber_bp.route('/start', methods=['GET', 'POST'])
def start():
    page = build_test_route(test_name="bit_error_ratio")
    return render_template('test_outputs/test_output.html', page=page)
