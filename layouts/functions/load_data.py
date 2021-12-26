import pandas as pd
import numpy as np


def import_members():
    df = pd.read_csv("layouts/data/members.csv")
    return df


def import_playlists():
    df = pd.read_csv("layouts/data/playlists.csv")
    # Create Month column
    df["month"] = df["name"].str.lower().str.replace("skype chat ", "").str.title()
    df["month"] = np.where(df["month"] == "Feb", "February", df["month"])
    return df


def import_tracks():
    df = pd.read_csv("layouts/data/tracks.csv")
    return df

