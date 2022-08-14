import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.losses import SparseCategoricalCrossentropy
import plotly.express as px
import matplotlib.pyplot as plt

from layouts.functions.load_data import *


def widgvis(fig):
    fig.canvas.toolbar_visible = False
    fig.canvas.header_visible = False
    fig.canvas.footer_visible = False


def plot_loss_tf(history):
    fig, ax = plt.subplots(1, 1, figsize=(4, 3))
    widgvis(fig)
    ax.plot(history.history["loss"], label="loss")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("loss (cost)")
    ax.legend()
    ax.grid(True)
    plt.show()


# Load data --------------
members = import_members()
artists = import_artists()
tracks = import_tracks()
playlists = import_playlists()

combined_df = pd.merge(tracks, members, how="left", on="added_by.id")

# Cleaning
combined_df["release_date"] = pd.to_datetime(
    combined_df["track.album.release_date"], infer_datetime_format=True
)
combined_df["release_date_seconds"] = (
    combined_df["release_date"].astype("datetime64").astype(int).astype(float)
)

# Calculate sone aggregate features
combined_df = (
    combined_df.groupby(["display_name", "playlist_id"])
    .agg(
        track_duration_average=("track.duration_ms", np.mean),
        explicit_any=("track.explicit", np.any),
        release_date_seconds=("release_date_seconds", np.max),
        track_popularity_max=("track.popularity", np.max),
        artist=(
            "artist.id",
            lambda x: pd.Series.mode(x)[0],
        ),  # I previously included this in the group by but this created loads of roads when there were multiple artists, so i just take the one that appears the most
    )
    .reset_index()
    .rename(columns={"artist": "artist.id"})
)

# Merge on artist info
df = pd.merge(combined_df, artists, how="left", on="artist.id")

# Add playlist
df = pd.merge(df, playlists[["id", "month"]], left_on="playlist_id", right_on="id")

# EDA ------------
def plot_by_user(df, feature):

    fig = px.strip(df, x="display_name", y=feature, stripmode="overlay")

    return fig


# if __name__ == "__main__":
# plot_by_user(df, "release_date_seconds").show()
# plot_by_user(df, "explicit_any").show()
# plot_by_user(df, "track_popularity_max").show()
# plot_by_user(df, "popularity").show()


# Split into testing, cv, and training -------------
# First we restrict to just paramters we think will be predictive
df = df.drop(["artist.id", "playlist_id", "id"], axis=1)

# # Try smaller subset
# df = df[
#     [
#         "display_name",
#         "track_duration_average",
#         "explicit_any",
#         "release_date_seconds",
#         "track_popularity_max",
#         "popularity",
#         "month",
#     ]
# ]

test_df = df[df["month"].isin(["January 2022", "March 2022"])]
cv_df = df[df["month"].isin(["November 2021", "December 2021"])]
train_df = df[
    ~df["month"].isin(["November 2021", "December 2021", "January 2022", "March 2022"])
]

# Check groups
train_df["display_name"].value_counts()


def create_X_y(df):
    X = df.drop(["display_name", "month", "Unnamed: 0", "name"], axis=1)
    X = tf.convert_to_tensor(np.asarray(X).astype(int))
    y_index = pd.DataFrame()
    y_index["display_name"] = pd.Categorical(df["display_name"])
    y_index["code"] = y_index["display_name"].cat.codes
    y = tf.convert_to_tensor(y_index["code"])
    return X, y, y_index


train_X, train_y, train_y_index = create_X_y(train_df)
cv_X, cv_y, cv_y_index = create_X_y(cv_df)

# Create model architecture --------
display_names_num = len(df["display_name"].unique())

model = Sequential(
    [
        tf.keras.Input(shape=(train_X.shape[1],)),  # specify input size
        ### START CODE HERE ###
        Dense(units=50, activation="relu"),
        Dense(units=25, activation="relu"),
        Dense(units=15, activation="relu"),
        Dense(units=display_names_num, activation="linear")
        ### END CODE HERE ###
    ],
    name="my_model",
)

# model.summary()

model.compile(
    loss=SparseCategoricalCrossentropy(from_logits=True),
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
)


history = model.fit(train_X, train_y, epochs=100)

# Not sure why but this crashes VScode after running:
# plot_loss_tf(history)

cv_predict = model.predict(cv_X)
tf.argmax(cv_predict, axis=1)

train_predict = model.predict(train_X)
tf.argmax(train_predict, axis=1)


# Diagnostic -----------
# import shap

tf.keras.utils.plot_model(model, show_shapes=True, rankdir="LR")
