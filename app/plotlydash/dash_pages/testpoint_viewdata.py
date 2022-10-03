import typing as t

import dash
from dash import html
from dash import dcc
from dash import ctx
from dash.dependencies import Output, Input
import plotly.graph_objects as go

from database_functions.mongodatabase_functions import MongoDatabaseFunctions


INPUT_VOLTAGE_DIV = "input_voltage_div"
INPUT_VOLTAGE_DIV_FORMAT = "voltage_{input_rail}_div"
INPUT_VOLTAGE_DROPDOWN_FORMAT = "voltage_{input_rail}_dropdown"
INPUT_VOLTAGE_LABEL_FORMAT = "voltage_{input_rail}_label"
TEMPERATURE_DIV = "temperature_div"
TEMPERATURE_DROPDOWN = "temperature_dropdown"
TEST_SELECTION_DIV = "test_selection_div"
TEST_SELECTION_DROPDOWN = "test_selection_dropdown"
TEST_CONTENT_DIV = "test_content_div"
PAGE_CONTENT_DIV = "page_content_div"
RUNID_DIV = "runid_div"

dash_app = dash.get_app()


dash.register_page(__name__,
                   path_template='/testpoint_viewdata/<testpoint>',
                   title="View Runid Data",
                   name="Runid Data",
                   description="Runid Description")

def layout(runid: int = None):
    if runid == None:
        return html.Div("No Runid Provided")
    else:
        runid = int(runid)
        assert type(runid) == int

        '''
        capture_data = MongoDatabaseFunctions.get_waveforms_by_runid(runid=int(runid))
        for data in capture_data:
            print(data)
        '''
        content = html.Div(id=PAGE_CONTENT_DIV, hidden=True,
                           children=[html.Div(id=TEST_CONTENT_DIV)])
        sidebar = sidebar_layout(runid=runid)
        return html.Div([
            sidebar,
            content
        ])

def sidebar_layout(runid):
    return html.Div(f"Sidebar: {runid}")