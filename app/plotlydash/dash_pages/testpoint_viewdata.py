import typing as t

import dash
from dash import html
from dash import dcc
from dash import ctx
from dash.dependencies import Output, Input
import plotly.graph_objects as go

from database_functions.mongodatabase_functions import MongoDatabaseFunctions