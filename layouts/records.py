# This tab will be all about the choices we have made

from dotenv import load_dotenv  # for python-dotenv method
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas

load_dotenv()

client_id = os.environ.get("client_id")
client_secret = os.environ.get("client_secret")

client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
