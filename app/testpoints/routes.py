import typing as t
from dataclasses import dataclass, field

from flask import render_template, jsonify, Markup, send_file, current_app, request
import requests
from Entities.Entities import ProjectEntity, PBAEntity, ReworkEntity, RunidEntity, WaveformCaptureEntity
from app.testpoints import bp
from io import BytesIO
import datetime

from database_functions.mongodatabase_functions import MongoDatabaseFunctions


@bp.route('/testpoints/<product>/testpoint/<testpoint>/runids', methods=("GET", "POST"))
def testpoint_review_by_product_runids(product, testpoint):
    runid_cursor = MongoDatabaseFunctions.get_testpoints_for_product_by_runid(product=product, testpoint=testpoint)

    return render_template('/testpoints/testpoint_review_by_product_runids.html',
                           runid_cursor=runid_cursor)
