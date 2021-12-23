import pandas as pd


def import_members():
    df = pd.read_csv("layouts/data/members.csv")
    return df


def import_playlists():
    df = pd.read_csv("layouts/data/playlists.csv")
    return df


def import_tracks():
    df = pd.read_csv("layouts/data/tracks.csv")
    return df

