import typing as t

from flask import request, url_for
from app.shared.Pages.website_page import PostProcessingPage

from app import celeryapp
from celery import group, chain
import json


def build_test_route(test_name: str) -> PostProcessingPage:
    test_title = test_name.replace("_", " ").title()

    req = request.args.get("request")

    task = celeryapp.send_task(name=test_name,
                               kwargs={"request": req})

    task_ids = [task.id]
    task_urls = [url_for('tasks.taskstatus', task_id=task_id) for
                 task_id in task_ids]

    page = PostProcessingPage(title=f"Post Processing - {test_title}",
                              header=test_title,
                              processing_header="Processing Request....",
                              task_urls=task_urls,
                              redirect_url=url_for(
                                  'post.download_result'))
    return page


def build_test_group_route(test_name: str) -> PostProcessingPage:
    test_title = test_name.replace("_", " ").title()

    req_list = json.loads(request.args.get("request"))

    task_ids = []
    for req in req_list:
        json_req = json.dumps(req)
        task = celeryapp.send_task(name=test_name,
                                  kwargs={"request": json_req})
        task_ids.append(task.id)

    task_urls = [url_for('tasks.taskstatus', task_id=task_id) for
                 task_id in task_ids]

    page = PostProcessingPage(title=f"Post Processing - {test_title}",
                              header=test_title,
                              processing_header="Processing Request....",
                              task_urls=task_urls,
                              redirect_url=url_for(
                                  'post.download_result'))
    return page
