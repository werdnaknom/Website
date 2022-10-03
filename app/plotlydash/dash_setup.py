import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input


def init_dash(server):
    """Create a Plotly Dash dashboard"""
    dash_app = dash.Dash(
        server=server,
        use_pages=True,
        pages_folder="plotlydash/dash_pages",
        routes_pathname_prefix='/dash/',
        #external_stylesheets=[dbc.themes.BOOTSTRAP]
    )

    dash_app.layout = html.Div(children=[
        dcc.Location(id='url', refresh=False),
        html.Div(children=[
            dash.page_container
        ])
    ])

    return dash_app.server
