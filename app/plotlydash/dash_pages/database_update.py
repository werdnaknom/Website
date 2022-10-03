import typing as t
from pathlib import Path
from threading import Thread

import dash
from dash import html
from dash import dcc
from dash import ctx
import dash_bootstrap_components as dbc
from flask import current_app
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from app.database_update.database_update import update_database

#OREGON_HARDDRIVE_LOC = current_app.config.get("DATADIRECTORY")
#KULIM_HARDDRIVE_LOC = current_app.config.get("KM_DATADIRECTORY")
OREGON_HARDDRIVE_LOC = "//npo/coos/LNO_Validation/Validation_Data/_data/ATS 2.0"
KULIM_HARDDRIVE_LOC = "//npo/coos/LNO_Validation/Kulim/ATS 2.0 Data"

HARDDRIVE_PATHS = [Path(OREGON_HARDDRIVE_LOC), Path(KULIM_HARDDRIVE_LOC)]

dash_app = dash.get_app()
dash_app.external_stylesheets = [dbc.themes.BOOTSTRAP]

dash.register_page(__name__,
                   path_template='/database_update',
                   title="Update",
                   name="Update",
                   description="Update Database with new data")


def harddrive_query(depth: int = 0, query: dict = dict) -> t.List[str]:
    result = set()
    for key, value in query.items():
        if value == "All":
            query[key] = "*"
    pattern_list = [query.get("product", "*"),
                    query.get("pba", "*"),
                    query.get("rework", "*"),
                    query.get("serial", "*"),
                    query.get("runid", "*"),
                    ]
    for harddrive in HARDDRIVE_PATHS:
        if depth != 0:
            pattern = "/".join(pattern_list[:depth + 1])
            result.update([x.name for x in harddrive.glob(pattern) if x.is_dir()])
        else:  # PRODUCT
            result.update([x.name for x in harddrive.iterdir() if x.is_dir()])
    return list(result)


def harddrive_query_products():
    return harddrive_query(depth=0, query={})


def harddrive_query_pba(query: dict, cur_list: t.List[str] = list):
    cur_list.extend(harddrive_query(depth=1, query=query))
    return cur_list


def harddrive_query_rework(query: dict, cur_list: t.List[str] = list):
    cur_list.extend(harddrive_query(depth=2, query=query))
    return cur_list


def harddrive_query_serial(query: dict, cur_list: t.List[str] = list):
    cur_list.extend(harddrive_query(depth=3, query=query))
    return cur_list


def harddrive_query_runid(query: dict, cur_list: t.List[str] = list):
    cur_list.extend(harddrive_query(depth=4, query=query))
    return cur_list


def layout():
    product_dropdown_div = html.Div(id="product_dropdown_div",
                                    children=[html.Label("Select Product To Update:"),
                                              dcc.Dropdown(harddrive_query_products(), clearable=False,
                                                           id='dropdown_product'),
                                              html.Br()])
    dropdown_div = html.Div(id='dropdown_div',
                            children=[
                                html.Div([html.Label("Select PBA:"),
                                          dcc.Dropdown(["All"], value="All", clearable=False, id='dropdown_pba'),
                                          ]),
                                html.Div([html.Label("Select Rework:"),
                                          dcc.Dropdown(["All"], value="All", clearable=False, id='dropdown_rework'),
                                          ]),
                                html.Div([html.Label("Select Serial:"),
                                          dcc.Dropdown(["All"], value="All", clearable=False, id='dropdown_serial'),
                                          ]),
                                html.Div([html.Label("Select Runid:", className="col-sm-2 col-form-label"),
                                          dcc.Dropdown(["All"], value="All", clearable=False, id='dropdown_runid')]),
                                html.Button('Update', id='submit_button', n_clicks=0, className="btn btn-primary")
                            ],
                            hidden=True)
    progress_div = html.Div(id="progress_div",
                            children=[dbc.Progress(id="progress_bar", value=0, color="success"),
                                      dcc.Interval(id='progress_interval', n_intervals=0, interval=50,
                                                   disabled=True)],
                            hidden=True)

    content = dbc.Container(id="content_container",
                            children=[html.H1("Database Update"), product_dropdown_div, dropdown_div, progress_div,
                                      dcc.Store(id="start_timer"), dcc.Store(id="end_timer")])
    return content


@dash_app.callback(
    Output(component_id='dropdown_div', component_property='hidden'),
    Input(component_id='dropdown_product', component_property='value')
)
def product_selected(product):
    if product == None:
        raise PreventUpdate
    else:
        return False


@dash_app.callback(
    Output("dropdown_pba", "options"),
    Output("dropdown_rework", "options"),
    Output("dropdown_serial", "options"),
    Output("dropdown_runid", "options"),
    Output("dropdown_pba", "value"),
    Output("dropdown_rework", "value"),
    Output("dropdown_serial", "value"),
    Output("dropdown_runid", "value"),
    Input("dropdown_div", 'hidden'),
    State('dropdown_product', 'value')
)
def update_dropdowns(hidden, product):
    if hidden:
        return [], [], [], [], "All", "All", "All", "All"
    else:
        query = {"product": product}
        pbas = harddrive_query_pba(query, cur_list=["All"])
        reworks = harddrive_query_rework(query, cur_list=["All"])
        serials = harddrive_query_serial(query, cur_list=["All"])
        runids = harddrive_query_runid(query, cur_list=["All"])
        return pbas, reworks, serials, runids, "All", "All", "All", "All"


@dash_app.callback(
    Output('start_timer', "data"),
    Output('progress_div', "hidden"),
    Input('submit_button', 'n_clicks'),
    State('dropdown_product', "value"),
    State('dropdown_pba', "value"),
    State('dropdown_rework', "value"),
    State('dropdown_serial', "value"),
    State('dropdown_runid', "value"),
    State("end_timer", "value"),
)
def submit_pushed(n_clicks, product, pba, rework, serial, runid, end_timer):
    if n_clicks == 0 and end_timer:
        return False, False
    if n_clicks == 1:
        query = {"product": product,
                 "pba": pba,
                 "rework": rework,
                 "serial": serial,
                 "runid": runid}
        for key, value in query.items():
            if value == "All":
                query[key] = "*"
        thread = Thread(target=update_database, args=(query,))
        thread.start()
        return True, False
    else:
        raise PreventUpdate


@dash_app.callback(
    Output("progress_bar", "value"),
    Output("progress_bar", "label"),
    Output("end_timer", "data"),
    # Output("progress_interval", "disabled"),
    Input("progress_interval", "n_intervals")
)
def update_progress(n):
    progress = min(n % 200, 100)
    if progress == 100:
        return 100, "Complete!", True
    return progress, f"{progress}%", False


@dash_app.callback(
    Output('progress_interval', "disabled"),
    Output('submit_button', "n_clicks"),
    Input('start_timer', 'data'),
    Input('end_timer', 'data'),
    State("submit_button", "n_clicks")
)
def restart_page(start_timer, end_timer, n_clicks):
    if start_timer is None and end_timer is False and n_clicks == 0:
        return True, 0
    elif start_timer and not end_timer and n_clicks != 0:
        return False, 100
    elif start_timer and end_timer and n_clicks != 0:
        return True, 0
    else:
        raise PreventUpdate
