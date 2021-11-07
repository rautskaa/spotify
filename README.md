The Spotify service is currently in a development mode and was not yet approved by Spotify. 
In order to use the service to create playlists, a Spotify account should be added to a Developer Dashboard. 
Please reach out to Aksana R. to assist with that. More information about development mode for Spotify apps can be found 
at https://developer.spotify.com/community/news/2021/05/27/improving-the-developer-and-user-experience-for-third-party-apps/

To start a server locally in terminal enter the command:
python3 spotify_service.py

Endpoint for getting top tracks per genre from Beatport that also exist on Spotify:
Request method: GET
Endpoint: http://127.0.0.1:5000/get_top_tracks
Parameter: genre
Example: http://127.0.0.1:5000/get_top_tracks?genre=house
Returns: top tracks as JSON objects array

Endpoint for creating a playlist on Spotify with top tracks per genre from Beatport that also exist on Spotify:
Request method: POST
Endpoint: http://127.0.0.1:5000/playlist
Parameter: genre
Example: http://127.0.0.1:5000/playlist?genre=house

Supported genres by the service:
'house'
'deep-house'
'afro-house'
'breaks-breakbeat-uk-bass'
'bass-club'
'bass-house'
'140-deep-dubstep-grime'
'dance-electro-pop'
'dj-tools'
'drum-bass'
'dubstep'
'electro-classic-detroit-modern'
'electronica'
'funky-house'
'hard-dance-hardcore'
'hard-techno'
'indie-dance'
'jackin-house'
'mainstage'
'melodic-house-techno'
'minimal-deep-tech'
'nu-disco-disco'
'organic-house-downtempo'
'progressive-house'
'psy-trance'
'tech-house'
'techno-peak-time-driving'
'techno-raw-deep-hypnotic'
'trance'
'trap-wave'
'uk-garage-bassline'



