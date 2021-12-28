# third party
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc


from .records import records_layout

music_club_explanation = """
**What is music club?**

Every month we each choose an album or a select number of songs by a particular artist. We spend the month listening to these songs, and then come together to rate and review them. This dashboard is a record of all of our good, bad and ugly choices.  
"""

dashboard_layout = dbc.Container(
    children=[
        html.Br(),
        dbc.Row(html.H1("Music Club"), justify="center", align="center"),
        html.Br(),
        html.Div(records_layout, style={"width": "80vw"}),
        html.Br(),
        html.Div(
            [html.Hr(), dcc.Markdown(music_club_explanation),], style={"width": "80vw"}
        ),
    ],
    fluid=True,
    style={
        "margin-left": "5rem",
        #    "margin-right": "2rem",
        #    "padding": "2rem 1rem",
    },
)
