# third party
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc

from .records import records_layout

dashboard_layout = dbc.Container(
    children=[
        html.Br(),
        html.H2("Music Club"),
        html.H3("A record of our good, bad and ugly choices"),
        html.Br(),
        html.Div(records_layout, style={"width": "80vw"}),
    ],
    fluid=True,
)
