from config import Config
from . import bp

from flask import send_from_directory


@bp.route('/display/<path:filename>')
def display_file(filename):
    return send_from_directory(Config.DATADIRECTORY, filename)


@bp.route('/download/<path:filename>')
def display_file(filename):
    return send_from_directory(Config.DATADIRECTORY, filename, as_attachment=True)
