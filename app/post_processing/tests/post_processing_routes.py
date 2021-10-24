import time
import json

from celery import chain, group, chord
from flask import request, send_file, url_for, redirect



from . import bp as pp_bp


@pp_bp.route('/start', methods=['GET', 'POST'])
def start():
    # Grab Request from post
    json_req = json.loads(request.args.get("request"))
    # Do something?

    return redirect(url_for(f'{json_req["test_name"]}.start',
                            request=json_req))

