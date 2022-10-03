import typing as t
from dataclasses import dataclass, field

from flask import render_template, jsonify, Markup, send_file, current_app, request
import requests
from Entities.Entities import ProjectEntity, PBAEntity, ReworkEntity, RunidEntity, WaveformCaptureEntity
from app.database_update import bp
from io import BytesIO
import datetime

from database_functions.mongodatabase_functions import MongoDatabaseFunctions


@bp.route('/database_update', methods=("GET", "POST"))
def database_update():
    return render_template('/database_update/database_update.html')
