from config import Config
from . import bp

from flask import send_from_directory, send_file


@bp.route('/download/<path:filename>')
def display_file(filename):
    return send_from_directory(Config.DATADIRECTORY, filename, as_attachment=True)


@bp.route('/display/<path:filename>')
def load_image(filename):
    print("loading {}".format(filename))
    return send_file(filename, mimetype='image/fig')
