import typing as t

import dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input, State
from dash import callback_context

from database_functions.mongodatabase_functions import MongoDatabaseFunctions

dash.register_page(__name__,
                   path_template='/runid_viewimage/<runid>',
                   title="View Runid Image",
                   name="Runid Image",
                   description="Runid Image")


def layout(runid: int = None):
    layout = html.Div(id='page_content', children=[
        dcc.Dropdown(""),
        # html.Img(id='image'),
        html.H5("hello world", id="image"),
        html.Button("Previous", id="previous_button"),
        html.Button("Next", id="next_button"),
        dcc.Store(id="capture_number"),
        dcc.Store(id="runid", data=runid)

    ])
    return layout


@dash.get_app().callback(Output("capture_number", "data"),
                         # Output("image", "src"),
                         Input("previous_button", "n_clicks"),
                         Input("next_button", "n_clicks"),
                         State("capture_number", "data"))
def update_capture_number(next_button, previous_button, number):
    MAX_CAPTURES = 999  # TODO:: Need to query database for this,although not everytime.
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if number is None:
        number = 1
    if "next_button" in changed_id:  # Next case
        number = number + 1
    else:  # Previous Case
        number = number - 1

    if number < 1:
        return 1
    elif number > MAX_CAPTURES:
        return number - 1
    else:
        return number


@dash.get_app().callback(Output("image", "children"),
                         Input("capture_number", "data"),
                         State("runid", "data"))
def update_image_src(capture_number, runid):
    print(f"update, {runid}, {capture_number}")
    capture = MongoDatabaseFunctions.get_runid_capture_image_and_information(runid=runid, capture=capture_number)
    print(capture)
    return f"hello world"
