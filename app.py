# stdlib
import logging

# third party
import dash
import dash_bootstrap_components as dbc

# enable logging
logging.basicConfig(level=logging.INFO)

# include external css and js
# TODO: review
external_js = [
    "https://code.jquery.com/jquery-3.4.1.slim.min.js",
    "https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js",
    "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js",
]

app = dash.Dash(
    __name__,
    external_scripts=external_js,
    external_stylesheets=[
        dbc.themes.LUX,
    ],
)
server = app.server
app.config.suppress_callback_exceptions = True
