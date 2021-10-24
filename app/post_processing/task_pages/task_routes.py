import typing as t

from flask import jsonify, send_file
from . import bp

from celery_worker import celeryapp


def groupstatus(task_id):
    task = celeryapp.GroupResult(task_id)
    raise NotImplementedError


@bp.route("/task/<task_id>")
def taskstatus(task_id):
    print(task_id)
    task = celeryapp.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
            response['filename'] = task.info['filename']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    print("RESPONSE", response)
    return jsonify(response)
