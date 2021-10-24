import typing as t
from io import StringIO
import csv
import json
from io import BytesIO, StringIO

from flask import render_template, flash, make_response, redirect, url_for, \
    jsonify, send_file, request, send_from_directory, abort
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os
import platform

import celery
import pandas as pd

from . import bp

from .models import UploadForm
from app import celeryapp
from pathlib import Path
# from app import current_app as app

from app.shared.Requests.requests import PostProcessingRequest


def convert_to_excel_file(files_dict: t.Dict[str, str]) -> \
        BytesIO:
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')

    for sheet_name, df_json in files_dict.items():
        df = pd.read_json(df_json)
        df.to_excel(writer, startrow=0, merge_cells=False,
                    sheet_name=sheet_name)

    writer.close()
    output.seek(0)

    return output


def create_processing_request(test_name: str, data_file: FileStorage,
                              input_file: FileStorage, filter_by: str
                              ) -> PostProcessingRequest:
    saved_data_filename, saved_data_path = PostProcessingRequest.save_file(
        file=data_file)
    saved_input_filename, saved_input_path = PostProcessingRequest.save_file(
        file=input_file)

    req = PostProcessingRequest(test_name=test_name,
                                data_filename=saved_data_filename,
                                data_file_path=saved_data_path,
                                user_input_filename=saved_input_filename,
                                user_input_file_path=saved_input_path,
                                filter_by=filter_by)

    return req


def create_processing_request_group(test_name: str,
                                    data_file_list: t.List[pd.DataFrame],
                                    input_file: FileStorage) -> \
        t.List[PostProcessingRequest]:
    request_list = []

    for data_file in data_file_list:
        saved_input_filename, saved_input_path = \
            PostProcessingRequest.save_duplicate_file(
                file=input_file)
        saved_data_filename, saved_data_path = \
            PostProcessingRequest.save_dataframe(df=data_file)

        req = PostProcessingRequest(test_name=test_name,
                                    data_filename=saved_data_filename,
                                    data_file_path=saved_data_path,
                                    user_input_filename=saved_input_filename,
                                    user_input_file_path=saved_input_path)
        request_list.append(req)

    return request_list


@bp.route("/download_result", methods=['GET', 'POST'])
def download_result():
    '''
    req = request.form
    print("REQUEST", req)
    data_dict = json.loads(req.get("data"))
    print(data_dict)
    filename = req.get("filename")
    print("FILENAME: ", filename)

    if filename is "":
        filename = "FileNameNotGiven"
    file = convert_to_excel_file(data_dict)

    return send_file(filename_or_fp=file,
                     as_attachment=True,
                     attachment_filename=f"{filename}.xlsx",
                     mimetype='text/plain')
    '''
    req = request.form
    result_path = json.loads(req.get("data"))
    p = Path(result_path)
    print(p)
    return send_from_directory(directory=p.parent, filename=p.name,
                               as_attachment=True)

@bp.route('/downloadExampleUserInput', methods=["GET"])
def download_example_user_input():
    try:
        return send_from_directory(directory='static/xlsx',
                                   filename="USERINPUT_Template.xlsx",
                                   as_attachment=True)
    except FileNotFoundError:
        abort(404)

@bp.route('/', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        test_selected = form.test_selector.data
        data_file = form.csv_file.data
        user_file = form.user_input_file.data
        filter_by = form.filter_by.data

        req = create_processing_request(test_name=test_selected,
                                        data_file=data_file,
                                        input_file=user_file,
                                        filter_by=filter_by)

        req = json.dumps(req.to_dict())

        # r = celeryapp.send_task(f'{test_selected}', args=task_request)

        return redirect(url_for(f'{test_selected}.start',
                                request=req))

    flash("File not uploaded")
    return render_template('test_input/test_input.html', form=form)


@bp.route('/start_group', methods=['GET', 'POST'])
def upload_group():
    form = UploadForm()
    if form.validate_on_submit():
        test_selected = form.test_selector.data
        data_file = form.csv_file.data
        user_file = form.user_input_file.data

        # Turn the FileStorage object into a BytesIO wrapper for SendFile
        # mem = BytesIO()
        # mem.write(f.read())
        # mem.seek(0)
        # Test Test
        # df = pd.read_csv(f)
        df = pd.read_csv(data_file)
        split_runids = df.groupby(by=["runid"])
        split_df_list = []
        for _, split_df in split_runids:
            split_df_list.append(split_df)

        req_list = create_processing_request_group(test_name=test_selected,
                                                   data_file_list=split_df_list,
                                                   input_file=user_file)

        req_json_list = json.dumps([req.to_dict() for req in req_list])

        # r = celeryapp.send_task(f'{test_selected}', args=task_request)

        return redirect(url_for(f'{test_selected}.start_group',
                                request=req_json_list))

    #flash("File not uploaded")
    return render_template('test_input/test_input.html', form=form)


@bp.route('/celery/<taskid>', methods=["GET"])
def check_task(taskid):
    task_id = taskid
    print(taskid)
    result = celery.result.AsyncResult(task_id, app=celeryapp)

    if result.ready():
        return result.get()
    return result.state
