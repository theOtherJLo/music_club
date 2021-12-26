import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd


from .functions.load_data import *
from app import app

# Load data
members = import_members()
playlists = import_playlists()
tracks = import_tracks()

# Table function ----------------------
# This function creates the main table based on inputs such as month and
# a cell that has been clicked on
def create_output_df(month, active_cell=None):

    chosen_playlist = playlists[playlists["month"] == month]
    playlist_tracks = tracks[tracks["playlist_id"] == chosen_playlist["id"].iloc[0]]

    # Join on member info
    combined_df = pd.merge(playlist_tracks, members, how="left", on="added_by.id")

    # If no album has been selected, we just show one album per row
    output_df = (
        combined_df[
            [
                "display_name",
                "artist.name",
                "track.album.name",
                "album.image",
                "track.album.total_tracks",
                "artist.uri",
            ]
        ]
        # Taking the maximum occorunces
        .groupby(["display_name"])
        .agg(lambda x: x.value_counts().index[0])
        .reset_index()
    )

    # Creating album image entry
    output_df["album.image"] = output_df["album.image"].apply(
        lambda x: f"![Album image]({x})"
    )

    output_df["id"] = output_df["track.album.name"]

    if active_cell is not None:

        selected_album = active_cell["row_id"]

        # An Album has been clicked, so now we need to expand the table to show the tracks
        selected_tracks_df = combined_df[
            ["track.name", "display_name", "track.preview_url"]
        ][combined_df["track.album.name"] == selected_album]

        selected_tracks_df["album.image"] = ""
        selected_tracks_df["id"] = selected_tracks_df["track.preview_url"]
        selected_tracks_df["preview"] = (
            selected_tracks_df["track.preview_url"].str.startswith("https").apply(str)
        )

        # Add this for sorting
        selected_tracks_df["display_name"] = selected_tracks_df[
            "display_name"
        ] + selected_tracks_df.index.map(str)

        output_df = output_df.append(selected_tracks_df).sort_values(by="display_name")
        output_df["display_name"] = np.where(
            output_df["album.image"] == "", "", output_df["display_name"]
        )

    else:
        output_df["track.name"] = ""

    return output_df


def create_initial_output_table(month):

    output_df = create_output_df(month)

    # Create data table
    output_table = dash_table.DataTable(
        id="music-table",
        columns=[
            {"name": "", "id": "album.image", "presentation": "markdown"},
            {"name": "Album", "id": "track.album.name"},
            {"name": "Artist", "id": "artist.name"},
            {"name": "Chosen by", "id": "display_name"},
        ],
        data=output_df.to_dict("records"),
        editable=False,
        style_as_list_view=True,
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=30,
        # style_data={"maxWidth": "100px",},
        style_cell_conditional=[
            {"if": {"column_id": "album.image"}, "width": "64px"},
            {
                "if": {"column_id": "track.album.name"},
                "textAlign": "left",
                "width": "10%",
            },
            {"if": {"column_id": "artist.name"}, "textAlign": "right", "width": "10%",},
            {
                "if": {"column_id": "display_name"},
                "textAlign": "right",
                "width": "10%",
            },
            {"if": {"column_id": "track.name"}, "textAlign": "center"},
        ],
        style_header={"backgroundColor": "white", "fontWeight": "bold", "fontSize": 20},
    )

    return output_table


# Audio preview ---------------
# This doesn't matter as it will be hidden at first
audio_filename = tracks["track.preview_url"].iloc[0]
audio = html.Audio(
    id="track-audio", src=audio_filename, controls=True, style={"display": "none"}
)

audio_layout = html.Div(
    children=[
        dbc.Row(
            [
                dbc.Col("Select a blue track to play a preview:", width=3),
                dbc.Col(audio, width=6),
            ]
        )
    ]
)

# Layout --------------


records_layout = html.Div(children=[audio_layout, create_initial_output_table("March")])

# Callbacks ----------------
style_data_conditional = [
    {
        "if": {"state": "active"},
        "backgroundColor": "rgba(150, 180, 225, 0.2)",
        "border": "1px solid blue",
    },
    {
        "if": {"state": "selected"},
        "backgroundColor": "rgba(0, 116, 217, .03)",
        "border": "1px solid blue",
    },
]


@app.callback(
    [
        Output("music-table", "style_data_conditional"),
        Output("music-table", "data"),
        Output("music-table", "columns"),
        Output("music-table", "selected_cells"),
        Output("music-table", "active_cell"),
        Output("track-audio", "src"),
        Output("track-audio", "style"),
    ],
    [Input("music-table", "active_cell")],
)
def update_selected_row_color(active):

    style = style_data_conditional.copy()
    if active:
        if active["row_id"] is not None:
            style.append(
                {
                    "if": {
                        "filter_query": '{track.album.name} eq "'
                        + active["row_id"]
                        + '"'
                    },
                    "backgroundColor": "rgba(150, 180, 225, 0.2)",
                    "border": "1px solid blue",
                },
            )
            style.append(
                {
                    "if": {"filter_query": '{display_name} = ""',},
                    "border": "none",
                    "backgroundColor": "white",
                }
            )
            # Make tracks look like a hyperlink if a preview is available:
            style.append(
                {
                    "if": {"filter_query": "{preview} = True",},
                    "textDecoration": "underline",
                    "color": "blue",
                }
            )

        output_columns = [
            {"name": "", "id": "album.image", "presentation": "markdown"},
            {"name": "Album", "id": "track.album.name"},
            {"name": "Track", "id": "track.name"},
            {"name": "Artist", "id": "artist.name"},
            {"name": "Chosen by", "id": "display_name"},
        ]
    else:
        output_columns = [
            {"name": "", "id": "album.image", "presentation": "markdown"},
            {"name": "Album", "id": "track.album.name"},
            {"name": "", "id": "track.name"},
            {"name": "Artist", "id": "artist.name"},
            {"name": "Chosen by", "id": "display_name"},
        ]

    output_df = create_output_df("March", active_cell=active)

    # If active["row_id"] is a track and not an album, we also output the track
    if active:

        if active["row_id"] is not None:
            selected_track = active["row_id"]
        else:
            selected_track = ""
    else:
        selected_track = ""

    if selected_track.startswith("https"):
        audio_track = selected_track
        audio_style = {"display": "block"}
    else:
        audio_track = None
        audio_style = {"display": "none"}

    output_data = output_df.to_dict("records")

    selected_cells = []
    active_cell = None

    return (
        style,
        output_data,
        output_columns,
        selected_cells,
        active_cell,
        audio_track,
        audio_style,
    )

