from dotenv import load_dotenv  # for python-dotenv method
import os

# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np
import requests
from requests.models import requote_uri
from spotipy.oauth2 import SpotifyOAuth


def get_token():
    scope = "playlist-read-collaborative"
    auth_manager = SpotifyOAuth(scope=scope)
    access_token = auth_manager.get_access_token(as_dict=True)

    return access_token


# TODO: Add auto toekn refresh
def spotify_query(access_token, request_url, **kwargs):
    headers = {
        "Authorization": "Bearer {token}".format(token=access_token["access_token"])
    }

    r = requests.get(request_url, headers=headers, params=kwargs)

    r = r.json()

    try:
        output = pd.json_normalize(r["items"])
    except:
        output = r
    return output


def get_music_club_playlists(access_token):

    df = spotify_query(
        access_token,
        request_url="https://api.spotify.com/v1/users/11173343040/playlists",
        limit=50,
    )
    df = df[df["name"].str.contains("Skype")]

    return df


def get_music_club_tracks(access_token):

    playlists = get_music_club_playlists(access_token)

    df = pd.DataFrame()

    for index, row in playlists.iterrows():
        tracks_df = spotify_query(access_token, request_url=row["tracks.href"])
        tracks_df["playlist_id"] = row.id
        df = df.append(tracks_df)

    df["artist.name"] = df["track.album.artists"].apply(lambda x: x[0]["name"])
    df["artist.uri"] = df["track.album.artists"].apply(lambda x: x[0]["uri"])
    df["album.image"] = df["track.album.images"].apply(
        lambda x: x[-1]["url"]
    )  # Should take the smallest image (can change later)

    return df


def get_display_name(user_href):
    user_info = spotify_query(access_token, request_url=user_href)
    return user_info["display_name"]


def get_music_club_members(access_token):
    tracks = get_music_club_tracks(access_token)

    user_info = tracks[["added_by.href", "added_by.id"]].drop_duplicates()
    user_info["display_name"] = user_info["added_by.href"].apply(get_display_name)

    user_info["display_name"] = np.select(
        [
            user_info["display_name"] == "danelk1",
            user_info["display_name"] == "duuuncaaan",
            user_info["display_name"] == "11173343040",
            True,
        ],
        ["Dan Bright", "Duncan Stewart", "James Lowe", user_info["display_name"]],
    )

    user_info = user_info[
        ~user_info["display_name"].isin(["fionasarjantson", "sez0312"])
    ]

    return user_info


if __name__ == "__main__":
    access_token = get_token()
    playlists = get_music_club_playlists(access_token)
    tracks = get_music_club_tracks(access_token)
    members = get_music_club_members(access_token)

    playlists.to_csv("layouts/data/playlists.csv")
    tracks.to_csv("layouts/data/tracks.csv")
    members.to_csv("layouts/data/members.csv")

