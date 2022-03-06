import imports.spoti as spoti
import imports.tidal as tidal


def authorize():
    print("Initializing...\n")
    if not spoti.init() or not tidal.init():
        return False
    print("Initialization success!\n")
    return True


def main():
    if not authorize():
        print("Authorization failed!\nExiting...")
        return

    favs = spoti.getFavsSpoti()
    favs.reverse()
    tidal.checkFavsTidal()
    for idx, item in enumerate(favs):
        track = item['track']
        tidal.addToFavsTidal(
            artists=track['artists'],
            track_name=track['name'])
    print("\n\n\nTransfer finished!\n\n\n")
    missing = tidal.getMissing()
    if missing:
        print("Some track are missing. Check out this list to see, what are they:")
        for idx, track in enumerate(missing):
            print(track)


if __name__ == "__main__":
    main()
