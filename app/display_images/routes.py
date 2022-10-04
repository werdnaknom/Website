from config import Config
from . import bp

from flask import send_from_directory, send_file


from pathlib import Path

@bp.route('/download/<path:filename>')
def display_file(filename):
    return send_from_directory(Config.DATADIRECTORY, filename, as_attachment=True)


@bp.route('/display/<path:filename>')
def load_image(filename):
    if not Path(filename).exists():
        filename = filename.replace("\\", "/")
    filepath = Path(filename)
    return send_file(filepath, mimetype='image/fig')
