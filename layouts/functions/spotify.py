from dotenv import load_dotenv  # for python-dotenv method
import os

# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import requests
from requests.models import requote_uri
from spotipy.oauth2 import SpotifyOAuth


# def spotify_login():
#     load_dotenv()

#     client_id = os.environ.get("client_id")
#     client_secret = os.environ.get("client_secret")

#     client_credentials_manager = SpotifyClientCredentials(
#         client_id=client_id, client_secret=client_secret
#     )

#     sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#     return sp


def get_token():
    load_dotenv()

    client_id = os.environ.get("client_id")
    client_secret = os.environ.get("client_secret")
    redirect_uri = os.environ.get("redirect_uri")
    scope = "playlist-read-collaborative"

    AUTH_URL = "https://accounts.spotify.com/api/authorize"

    # POST
    auth_response = requests.post(
        AUTH_URL,
        {
            # "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "scope": scope,
        },
    )

    # convert the response to JSON
    auth_response_data = auth_response.json()

    # save the access token
    access_token = auth_response_data["access_token"]

    return access_token


def spotify_query(access_token, endpoint, **kwargs):
    headers = {"Authorization": "Bearer {token}".format(token=access_token)}

    # base URL of all Spotify API endpoints
    REQUEST_URL = "https://api.spotify.com/v1/" + endpoint

    # for key, value in kwargs.items():
    #     if key == list(kwargs)[0]:
    #         REQUEST_URL = REQUEST_URL + "?" + key + "=" + str(value)
    #     else:
    #         REQUEST_URL = REQUEST_URL + "&" + key + "=" + str(value)

    # actual GET request with proper header
    r = requests.get(REQUEST_URL, headers=headers, params=kwargs)

    r = r.json()

    try:
        output = pd.json_normalize(r["items"])
    except:
        output = r
    return output


def get_music_club_playlists(access_token):

    df = spotify_query(access_token, endpoint="users/11173343040/playlists", limit=50)
    df["name"]


spotify_query(access_token, endpoint="me")

scope = "playlist-read-collaborative"
auth_manager = SpotifyOAuth(scope=scope)
access_token = auth_manager.get_access_token(as_dict=False)
