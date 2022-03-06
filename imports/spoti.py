import spotipy
from spotipy.oauth2 import SpotifyOAuth


def init():
    scope = "user-library-read"
    global session
    session = spotipy.Spotify(auth_manager=SpotifyOAuth(
        scope=scope,
        client_id="feb2a8030a2f42899d4bf62a21ba29b2",
        client_secret="4a31a060f0a14d88b77c03bec617115a",
        redirect_uri="http://localhost:9999"))
    if not session.current_user:
        return False
    return True


def getFavsSpoti():

    favorites_spoti = []
    multipl_index = 1
    multiplier = 50

    res = session.current_user_saved_tracks(limit=50)
    favorites_spoti = res['items']

    while len(res['items']) == 50:
        res = session.current_user_saved_tracks(
            limit=50, offset=multiplier*multipl_index)
        favorites_spoti += res['items']
        multipl_index += 1

    print("Total amount of songs to transfer:", len(favorites_spoti))
    return favorites_spoti
