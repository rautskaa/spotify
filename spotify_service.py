import spotify_functions
from flask import Flask, request

app = Flask(__name__)


@app.route("/top-tracks")
def get_top_tracks():
    """HTTP GET request to get top tracks from Beatport based on genre which also exist on Spotify
    Example of end point: http://127.0.0.1:5000/top-tracks?genre=house
    :return array of JSON objects with top tracks (song, artist, track_id)
     """
    genre = request.args.get("genre")
    top_tracks = spotify_functions.get_top_tracks(genre)
    return top_tracks


@app.route("/playlist", methods=["POST"])
def create_playlist():
    """HTTP POST request to create a Spotify playlist based on genre with top tracks from Beatport
    which also exist on Spotify. Example of end point: http://127.0.0.1:5000/playlist?genre=house
    :return created playlist
    """
    genre = request.args.get("genre")
    playlist = spotify_functions.create_playlist_with_top_tracks(genre)
    return playlist


if __name__ == '__main__':
    app.run()
