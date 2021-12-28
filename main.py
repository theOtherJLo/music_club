#!/usr/bin/env python3
# load in environment variables and logging
# stdlib
import os
import logging
import random

# third party
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


# project
from app import app, server
from layouts import dashboard_layout

logging.info("Setting main layout")


app.layout = html.Div(children=dashboard_layout, className="row pl-5")


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)
