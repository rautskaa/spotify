import configparser
import json
import sys
import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth

# Parse config file "config.cfg"
config = configparser.ConfigParser()
config.read('config.cfg')
client_id = config.get('SPOTIFY', 'CLIENT_ID')
client_secret = config.get('SPOTIFY', 'CLIENT_SECRET')
# Setting scope requires for creating a playlist
scope = 'playlist-modify-public'
# Authenticate to Spotify
# redirect_uri is launched with the window where user gives permission for the service to use their Spotify data
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret,
                                                    redirect_uri='http://localhost:8888/'))


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
    top_tracks = get_top_tracks(genre)
    # Add items to a playlist when looping through json and getting tracks
    # Load JSON string into a dictionary
    json_dict = json.loads(top_tracks)
    for track in json_dict:
        track_id = track['track_id']
        spotify.playlist_add_items(playlist_id, track_id, position=None)
    print("=== Created a playlist for " + genre + " on Spotify ===")
    print(playlist_result)
    return playlist_result


def create_playlist(genre):
    """Create a playlist on Spotify per given genre.
      :param genre
      :return created playlist
      """
    print("Creating a playlist on Spotify...")
    user_id = get_user_id()
    genre_title = get_genres_title()
    playlist_title = genre_title[genre].upper() + " TOP TRACKS "
    result = spotify.user_playlist_create(user_id, playlist_title,
                                          public=True)
    return result


def get_genres():
    """Get dictionary of all supported genres on Beatport
      :return dictionary of genres
      """
    genres = {'house': 5,
              'deep-house': 12,
              'afro-house': 89,
              'breaks-breakbeat-uk-bass': 9,
              'bass-club': 85,
              'bass-house': 91,
              '140-deep-dubstep-grime': 95,
              'dance-electro-pop': 39,
              'dj-tools': 16,
              'drum-bass': 1,
              'dubstep': 18,
              'electro-classic-detroit-modern': 94,
              'electronica': 3,
              'funky-house': 81,
              'hard-dance-hardcore': 8,
              'hard-techno': 2,
              'indie-dance': 37,
              'jackin-house': 97,
              'mainstage': 96,
              'melodic-house-techno': 90,
              'minimal-deep-tech': 14,
              'nu-disco-disco': 50,
              'organic-house-downtempo': 93,
              'progressive-house': 15,
              'psy-trance': 13,
              'tech-house': 11,
              'techno-peak-time-driving': 6,
              'techno-raw-deep-hypnotic': 92,
              'trance': 7,
              'trap-wave': 38,
              'uk-garage-bassline': 86}
    return genres


def get_genres_title():
    """Get dictionary of titles all supported genres on Beatport
    :return title
    """
    genres = {'house': 'house',
              'deep-house': 'deep house',
              'afro-house': 'afro house',
              'breaks-breakbeat-uk-bass': 'breaks / breakbeat / uk bass',
              'bass-club': 'bass / club',
              'bass-house': 'bass house',
              '140-deep-dubstep-grime': '140 / deep dubstep / grime',
              'dance-electro-pop': 'dance / electro pop',
              'dj-tools': 'dj tools',
              'drum-bass': 'drum & bass',
              'dubstep': 'dubstep',
              'electro-classic-detroit-modern': 'electro (classic / detroit / modern)',
              'electronica': 'electronica',
              'funky-house': 'funky house',
              'hard-dance-hardcore': 'hard dance / hardcore',
              'hard-techno': 'hard techno',
              'indie-dance': 'indie dance',
              'jackin-house': 'jackin house',
              'mainstage': 'mainstage',
              'melodic-house-techno': 'melodic house & techno',
              'minimal-deep-tech': 'minimal / deep tech',
              'nu-disco-disco': 'nu disco / disco',
              'organic-house-downtempo': 'organic house / downtempo',
              'progressive-house': 'progressive house',
              'psy-trance': 'psy-trance',
              'tech-house': 'tech house',
              'techno-peak-time-driving': 'techno (peak time / driving)',
              'techno-raw-deep-hypnotic': 'techno (raw / deep / hypnotic)',
              'trance': 'trance',
              'trap-wave': 'trap / wave',
              'uk-garage-bassline': 'uk garage / bassline'}
    return genres


def get_beatport_url(genre):
    """Get Beatport url with top tracks
    :param url, example "https://www.beatport.com/genre/deep-house/12/top-100"
    :return url
    """
    genres = get_genres()
    if genre in genres:
        converted_num = str(genres[genre])
        url = "https://www.beatport.com/genre/" + genre + "/" + converted_num + "/" + "top-100"
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
    print("Finding top tracks on Spotify for genre", genre, "from Beatport...")
    result_dict = {}
    result_top_tracks = {}
    url = get_beatport_url(genre)
    songs = []
    artists = []
    track_ids = []

    results = scrap_tracks_from_beatport(url)
    for i in range(0, 100):
        song_name = results[i]['data-ec-name']
        artist = results[i]['data-ec-d1']
        result_dict[song_name] = artist
        # Search song in spotify catalog with exact match
        search_result = spotify.search(song_name, limit=10, offset=0, type='track', market=None)
        prev_track = ""
        for item in search_result["tracks"]["items"]:
            if item["name"] == song_name and prev_track != item["name"]:
                for artist_ in item["artists"]:
                    # If artist matches the song name, get track id
                    if artist_["name"] == artist:
                        track_id = [item["id"]]
                        track_ids.append(track_id)
                        songs.append(song_name)
                        artists.append(artist)
                        prev_track = item["name"]
    json_data = convert_to_json(songs, artists, track_ids)
    print("=== Found top tracks on Spotify from Beatport ===")
    print(json_data)
    return json_data


if __name__ == '__main__':
    genre = sys.argv[1]
