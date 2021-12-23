# third party
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc

# project
from app import app
from .functions.load_data import *

dashboard_layout = dbc.Container(
    children=[
        html.Br(),
        html.H2("Music Club"),
        html.H3("A record of our good, bad and ugly choices"),
        html.Br(),
        # html.Div(tabs, style={"width": "80vw"}),
    ],
    fluid=True,
)
