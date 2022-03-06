from urllib import request
from prompt_toolkit import prompt
import tidalapi
import requests

s = tidalapi.Session()
missing_in_tidal = []


def init():
    s.login_oauth_simple()

    global User
    User = s.user

    if not s.check_login():
        return False
    return True


def checkFavsTidal():
    favorites_tidal = User.favorites.tracks()

    if favorites_tidal:
        print("\nWarning!", "Tidal favorites library is not empty. We recommend that you start with an empty one!\n")
        if input("The following action will erase your Tidal favorites library. Are you sure? (y/n) ").lower() == "y":
            for idx, item in enumerate(favorites_tidal):
                User.favorites.remove_track(item.id)
            print("\nTidal library erased! Moving on...\n")
        else:
            print("\nMoving on as is...\n")
    else:
        print("\nNo Tidal favorites found! Moving on...\n")


def addToFavsTidal(artists, track_name):
    track_resolved = False
    for i, artist in enumerate(artists):
        id = findTrack(a=artist['name'], t=track_name)
        if not (id == -1):
            track_resolved = True
            User.favorites.add_track(id)
            break
    while not track_resolved:
        print("\nSeems like we were unable to find this track automatically:",
              artists[0]['name']+" "+track_name)
        valid_prompt = False
        while not valid_prompt:
            prompt = input("Would you like to provide a custom search query? (Sometimes our query misses the track because it's not named EXACTLY the same as in Spotify. You may try the same search query from above and we'll show you what was found according to these results!) (y/n): ").lower()
            if prompt == "y" or prompt == "n":
                valid_prompt = True

        if prompt == "y":
            id = findByQuery(input("Provide a query: "))
            if id == -1:
                continue
            track_resolved = True
            User.favorites.add_track(id)
        elif prompt == "n":
            track_resolved = True
            missing_in_tidal.append(artists[0]['name']+" "+track_name)


def findTrack(a, t):
    search = s.search(field="track", value=a+" "+t)

    if len(search.tracks) == 0:
        return -1

    for idx, track in enumerate(search.tracks):
        if checkArtist(track.name.lower(), t.lower()) and checkTrackName(track.artist.name.lower(), a.lower()):
            return track.id
    return -1


def findByQuery(q):
    search = s.search(field="track", value=q)

    if len(search.tracks) == 0:
        return -1

    for idx, track in enumerate(search.tracks):
        pmpt = input("Is this right? " + track.artist.name + " - " + track.name + (" ("+track.version+")" if track.version else "") + " (y/n/q) ").lower()
        if pmpt == "y":
            return track.id
        elif pmpt == "q":
            return -1


def checkArtist(source, target):
    res = source.find(target)
    if res != -1:
        return True
    else:
        return False


def checkTrackName(source, target):
    res = source.find(target)
    if res != -1:
        return True
    else:
        return False


def getMissing():
    return missing_in_tidal
