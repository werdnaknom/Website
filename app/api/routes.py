from config import Config
from . import bp
import json

from pathlib import Path

from flask import make_response, jsonify, request

@bp.route('/api/add_project', methods=["POST", "GET"])
def api_add_project():
    content_type = request.headers.get('Content-Type')
    data = json.loads(request.data)
    p = Path(data["path"])
    print(p.exists())
    return jsonify("hello")