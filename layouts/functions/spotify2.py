import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import pandas as pd


def authenticate_spotify(scope="playlist-read-collaborative"):
    load_dotenv()

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    return sp


def get_music_club_playlists_df(sp):
    playlists = sp.current_user_playlists(limit=50)
    df = pd.DataFrame(playlists["items"])

    df = df[df["name"].str.contains("Skype")]


if __name__ == "__main__":
    sp = authenticate_spotify()
    df = get_music_club_playlists_df(sp)

    df["tracks"]

