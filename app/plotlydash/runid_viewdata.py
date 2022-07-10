import re
from typing import Collection
import logging

import dash
from dash import html
from dash import dcc
from dash import dash_table
from dash_table import DataTable
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd







def init_dash(server):
    """Create a Plotly Dash dashboard"""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/runid_viewdata/',
        #url_base_pathname='/runid_viewdata/',
        # external_stylesheets=[
        #    '/static/dist/css/styles.css'
        # ]
    )

    # Create Dash Layout
    dash_app.layout = html.Div([
        html.H1("Hello World"),
        dcc.Dropdown(id="project_dropdown",
                     options=["a", 'b', "c"],
                     multi=True,
                     placeholder="Select a Project"),
        html.Div(id="test_content",
                 children="YES!"),
        dcc.Location(id='url', refresh=False),
    ],
        id="dash-container")

    init_callbacks(dash_app)

    return dash_app.server


def init_callbacks(dash_app):
    @dash_app.callback(Output("test_content", "children"),
                       Input("project_dropdown", "value"))
    def update_test_content(pathname):
        return pathname


'''

def init_callbacks(dash_app):
    @dash_app.callback(Output("pba_dropdown", "options"), Output("pba_dropdown", "disabled"),
                       Input("project_dropdown", "value"))
    def update_pba_dropdown_by_project(project):
        if project == None:
            logging.debug(msg="UPDATE_PBA_DROPDOWN_BY_PROJECT --> NONE")
            return [], True
        pbas = search_project_pbas(project)
        logging.debug(
            msg="UPDATE_PBA_DROPDOWN_BY_PROJECT --> PROJECT: {project}, result PBA: {pba}".format(project=project,
                                                                                                  pba=pbas))
        return pbas, False

    @dash_app.callback(Output("textarea-example", 'value'),
                       Input("pba_dropdown", "value"))
    def update_textbox_with_runids(pbas):
        print(pbas)
        runids = search_runid_by_pba_status(pba_list=pbas, status=None)
        runid_str = ", ".join([str(runid) for runid in runids])
        return runid_str

    @dash_app.callback(Output("tables_container", "children"),
                       Input("pba_dropdown", "value"))
    def update_table(pba_list):
        runids = return_full_runid(pba_list)
        df = pd.DataFrame(runids)
        table = DataTable(id="runid_datatable",
                          data=df.to_dict('records'),
                          filter_options={"case": "insensitive"},
                          sort_action="native",
                          # sort_by=[{'runid': 'desc'}]

                          )

        return table
'''
