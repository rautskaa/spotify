import configparser
import json
import sys
import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
from genres import get_genres_num, get_genres_title


# Authentication for Spotify API use
config = configparser.ConfigParser()
config.read('config.cfg')
id = config.get('SPOTIFY', 'CLIENT_ID')
secret = config.get('SPOTIFY', 'CLIENT_SECRET')
scope = 'playlist-modify-public'
# redirect_uri launches browser for user to give permission to use their Spotify data
uri = 'http://localhost:8888/'
auth_manager = SpotifyOAuth(scope=scope, client_id=id, client_secret=secret, redirect_uri=uri)
spotify = spotipy.Spotify(auth_manager=auth_manager)


def get_user_id():
    """Get a Spotify user id.
    return user_id
    """
    user = spotify.me()
    user_id = user['id']
    return user_id


def create_playlist_with_top_tracks(genre):
    """Create a playlist on Spotify with top tracks per given genre.
    :param genre
    :return created playlist
    """
    playlist_result = create_playlist(genre)
    playlist_id = playlist_result['id']
    print("Finding top tracks on Spotify for genre", genre, "from Beatport...")
    top_tracks = get_top_tracks(genre)  # Load JSON string into a dictionary
    # Add items to a playlist when looping through json and getting tracks
    json_dict = json.loads(top_tracks)
    for track in json_dict:
        track_id = track['track_id']
        spotify.playlist_add_items(playlist_id, track_id, position=None)
    print("=== Created a playlist for " + genre + " on Spotify ===\n", playlist_result)
    return playlist_result


def create_playlist(genre):
    """Create a playlist on Spotify per given genre.
      :param genre
      :return created playlist
      """
    print("Creating a playlist on Spotify...")
    user_id = get_user_id()
    genre_title = get_genres_title()
    selected_genre = ''.join(genre_title[genre])
    playlist_title = selected_genre.upper() + " TOP TRACKS "
    result = spotify.user_playlist_create(user_id, playlist_title,
                                          public=True)
    return result

def get_beatport_url(genre):
    """Get Beatport url with top tracks
    :param url, example "https://www.beatport.com/genre/deep-house/12/top-100"
    :return url
    """
    genres = get_genres_num()
    if genre in genres:
        num_as_str = str(genres[genre])
        num = num_as_str.replace("{","").replace("}", "")
        url = "https://www.beatport.com/genre/" + genre + "/" + num + "/" + "top-100"
        print("=== Beatport URL with top tracks for " + genre + " ===")
        print(url)
        return url


def convert_to_json(songs, artists, track_ids):
    """Convert data to JSON
     :param songs
     :param artists
     :param track_ids
     :return array of JSON objects
     """
    data = [{"Song": s, "Artist": a, "track_id": t} for s, a, t in zip(songs, artists, track_ids)]
    json_data = json.dumps(data)
    print("=== Found top tracks on Spotify from Beatport ===\n" + json_data)
    return json_data


def scrap_tracks_from_beatport(url):
    """Scrap top tracks from Beatport using BeautifulSoup
     :param url with top tracks
     :return results
     """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all(class_="bucket-item ec-item track")
    return results


def get_top_tracks(genre):
    """Get top tracks from Beatport which also exist on Spotify
     :param genre
     :return array of JSON objects with top tracks (song, artist, track_id)
     """
    result_dict = {}
    songs, artists, track_ids = ([] for i in range(3))
    results = scrap_tracks_from_beatport(get_beatport_url(genre))
    for i in range(0, 100):
        song_name, artist = results[i]['data-ec-name'], results[i]['data-ec-d1']
        result_dict[song_name] = artist
        song_data = []
        song_data.extend((track_ids, songs, artists))
        search_song(song_name, artist, song_data)
    json_data = convert_to_json(songs, artists, track_ids)
    return json_data


def search_song(song_name, artist, song_data):
    """Append song to result if Beatport song exists in Spotify catalog
    :param song_name
    :param artist
    :param song_data"""
    # Search song in spotify catalog with exact match
    spotify_result = spotify.search(song_name, limit=10, offset=0, type='track', market=None)
    prev_track = ""
    track_ids, songs, artists = song_data[0], song_data[1], song_data[2]
    for item in spotify_result["tracks"]["items"]:
        if item["name"] == song_name and prev_track != item["name"]:
            for artist_ in item["artists"]:
                if artist_["name"] == artist:  # If artist matches the song name, append to result
                    track_id, prev_track = [item["id"]], item["name"]
                    track_ids.append(track_id)
                    songs.append(song_name)
                    artists.append(artist)


if __name__ == '__main__':
    genre = sys.argv[1]
