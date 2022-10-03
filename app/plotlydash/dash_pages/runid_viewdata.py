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
                   path_template='/runid_viewdata/<runid>',
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


def make_emtpy_fig() -> go.Figure:
    fig = go.Figure()
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig.layout.plot_bgcolor = "#E5ECF6"
    return fig


'''
def aux_to_main_graph(runid, temperatures):
    #print("FIG")
    fig = make_emtpy_fig()
    if not runid:
        return fig
    #print(runid)

    overall_max = 0
    overall_min = 9999

    # waveforms = MongoDatabaseFunctions.get_waveforms_by_runid(runid=runid)
    waveforms = MongoDatabaseFunctions.get_waveforms_for_aux_to_main_graph(runid=runid, temperatures=temperatures,
                                                                           voltages=[],
                                                                           scope_channels=[], test_category=)

    for wf in waveforms:
        x = wf['downsample'][0]
        y = wf['downsample'][1]
        fig.add_scatter(x=x, y=y)

    fig.layout.title = runid

    return fig
'''


def input_voltage_dropdown(input_voltage_groups: t.List) -> html.Div:
    voltage_dropdowns = [
        html.H5("Input Voltage Selection:")
    ]
    channels_added = []
    channels_skipped = []
    for i, input_rail in enumerate(input_voltage_groups):
        channel_setup = input_rail["_id"]
        channel_hidden = True
        voltage_channel = channel_setup.get("channel", None)
        voltage_group = channel_setup.get("group", None)
        voltage_voltages = input_rail.get("voltages", [])
        voltage_channel_number = channel_setup.get("channel_number", None)
        if channel_setup.get("channel_on", False):
            channels_added.append(voltage_channel_number)
            channel_hidden = False
        else:
            channels_skipped.append(voltage_channel_number)
            continue
        voltage_dropdowns.append(html.Div(id=INPUT_VOLTAGE_DIV_FORMAT.format(input_rail=voltage_channel_number),
                                          hidden=channel_hidden,
                                          children=[
                                              html.H5(
                                                  f'{voltage_channel} (Group: {voltage_group})'),
                                              dcc.Dropdown(
                                                  id=INPUT_VOLTAGE_DROPDOWN_FORMAT.format(
                                                      input_rail=voltage_channel_number),
                                                  value=voltage_voltages[0],
                                                  options=voltage_voltages,
                                                  multi=True
                                              )
                                          ]))
    # FOR CHANNEL "OFF" Case
    for channel_number in channels_skipped:
        if channel_number not in channels_added:
            # Add a fake channel that is off
            voltage_dropdowns.append(html.Div(id=INPUT_VOLTAGE_DIV_FORMAT.format(input_rail=channel_number),
                                              hidden=True,
                                              children=[
                                                  dcc.Dropdown(
                                                      id=INPUT_VOLTAGE_DROPDOWN_FORMAT.format(
                                                          input_rail=channel_number),
                                                      value=[],
                                                      options=[],
                                                      multi=True
                                                  )
                                              ]))

    return html.Div(id=INPUT_VOLTAGE_DIV, children=voltage_dropdowns, hidden=True)


def temperature_dropdown(temperature_list: t.List[int]) -> html.Div:
    return html.Div(id=TEMPERATURE_DIV, children=[
        html.H5("Temperature Selection:"),
        dcc.Dropdown(id=TEMPERATURE_DROPDOWN,
                     value=temperature_list,
                     options=temperature_list,
                     multi=True)],
                    hidden=True)


def test_selection_dropdown(test_categories: t.List) -> html.Div:
    return html.Div(id=TEST_SELECTION_DIV, children=[
        html.H5("Test Category Selection:"),
        dcc.Dropdown(id=TEST_SELECTION_DROPDOWN,
                     options=test_categories,
                     placeholder="Select a Test Category"),
    ])


def sidebar_layout(runid: int) -> html.Div:
    tests = MongoDatabaseFunctions.get_runid_test_categories(runid=runid)
    runid_div = html.Div(id=RUNID_DIV, hidden=True, children=runid)
    temperature_result, voltage_groups = MongoDatabaseFunctions.get_runid_capture_data(runid=runid)
    test_layout = test_selection_dropdown(test_categories=tests)
    voltage_layout = input_voltage_dropdown(input_voltage_groups=voltage_groups)
    temperature_layout = temperature_dropdown(temperature_result)
    sidebar = html.Div(id="sidebar_div", children=[
        runid_div,
        test_layout,
        temperature_layout,
        voltage_layout
    ])
    return sidebar


def aux_to_main_content(runid, test_category, test_parameters):
    waveforms = MongoDatabaseFunctions.get_waveforms_for_aux_to_main_graph(test_category=test_category, runid=runid,
                                                                           temperatures=test_parameters["temperatures"],
                                                                           voltages=test_parameters["voltages"],
                                                                           scope_channels=test_parameters["channels"])

    fig = make_emtpy_fig()
    waveforms = list(waveforms)
    fig.layout.title = f"{test_category} -- {len(waveforms)} Waveforms"
    colors = ['yellow', 'teal', 'red', 'green', 'orange', 'blue', 'maroon', 'light green']
    waveform_colors = {}
    for wf in waveforms:
        testpoint = wf.get("testpoint", "invalid testpoint")
        x = wf['downsample'][0]
        y = wf['downsample'][1]
        if testpoint in waveform_colors:
            color = waveform_colors[testpoint]
            fig.add_scatter(x=x, y=y, marker=dict(color=color), name=testpoint)
        else:
            color = colors[len(waveform_colors) - 1]
            waveform_colors[testpoint] = color
            fig.add_scatter(x=x, y=y, name=testpoint, marker=dict(color=color))

    return [dcc.Graph(id="aux_to_main_graph", figure=fig)]


def ethagent_content(test_category, test_parameters):
    return [f"no content for ethagent"]


@dash_app.callback(Output(INPUT_VOLTAGE_DIV, "hidden"),
                   Output(TEMPERATURE_DIV, "hidden"),
                   Input(TEST_SELECTION_DROPDOWN, "value"))
def test_category_selected(test_category):
    '''
    Unhides the sidebar contents when a test category is selected
    :param test_category:
    :return:
    '''
    if test_category == None:
        return True, True
    else:
        return False, False


@dash_app.callback(Output(PAGE_CONTENT_DIV, "hidden"),
                   Output(TEST_CONTENT_DIV, "children"),
                   Input(TEST_SELECTION_DROPDOWN, "value"),
                   Input(TEMPERATURE_DROPDOWN, "value"),
                   Input(INPUT_VOLTAGE_DROPDOWN_FORMAT.format(input_rail="0"), "value"),
                   Input(INPUT_VOLTAGE_DROPDOWN_FORMAT.format(input_rail="1"), "value"),
                   Input(INPUT_VOLTAGE_DROPDOWN_FORMAT.format(input_rail="2"), "value"),
                   Input(INPUT_VOLTAGE_DROPDOWN_FORMAT.format(input_rail="3"), "value"),
                   Input(RUNID_DIV, "children")
                   )
def test_content_viewer(test_category, temperature_list: t.List, voltage_0, voltage_1, voltage_2, voltage_3, runid):
    '''
    Displays the selected test content
    :param test_category:
    :return:
    '''
    test_parameters = {
        "temperatures": temperature_list,
        "voltages": {"0": voltage_0,
                     "1": voltage_1,
                     "2": voltage_2,
                     "3": voltage_3},
        "channels": []
    }
    if test_category == None:
        return True, None
    # elif test_category == "Aux To Main":
    #    return False, aux_to_main_content(runid=runid, test_category=test_category, test_parameters=test_parameters)
    elif test_category == "Ethagent":
        return False, ethagent_content(test_category, test_parameters)
    elif test_category == "Scripts":
        return False, f"No content for {test_category}...."
    else:
        return False, aux_to_main_content(runid=runid, test_category=test_category, test_parameters=test_parameters)
