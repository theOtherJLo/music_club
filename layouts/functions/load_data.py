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
    df["month"] = np.where(
        df["month"].str.contains("[0-9]"), df["month"], df["month"] + " 2021"
    )
    df = df[df["month"] != "May 2021"]
    return df


def import_tracks():
    df = pd.read_csv("layouts/data/tracks.csv")
    return df


def import_artists():
    df = pd.read_csv("layouts/data/artists.csv")
    return df
