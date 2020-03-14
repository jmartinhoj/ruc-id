import requests
import json
import os, sys
from acrcloud.recognizer import ACRCloudRecognizer
import secrets
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


token = ""
client_id = secrets.client_id
client_secret=secrets.client_secret
username = "ruc107.9"
playlist = "0eWYkGTWmlJtuLksLwMwBh"


def refresh():
    global token
    token = spotipy.util.prompt_for_user_token("ruc107.9",
        "playlist-modify-public",
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://localhost/")
    return

def main():
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    music = ""
    artist = ""
    config = {
        #Replace "xxxxxxxx" below with your project's host, access_key and access_secret.
        'host':'identify-eu-west-1.acrcloud.com',
        'access_key':'c20267418e799f23a3f94b14baf3a790', 
        'access_secret':'aiwwg7KPELXaWt9AwvfYv6IclZSCTndEltCftKjJ',
        'timeout':10 # seconds
    }
    re = ACRCloudRecognizer(config)
    while(1):
        os.system('sudo ./ripper.sh')


        json_data = json.loads(re.recognize_by_file("/tmp/aaa.mp3", 0))
        print(json.dumps(json_data))
        if(json_data["status"]["msg"] == "Success"):
            current_music = json_data["metadata"]["music"][0]["title"]
            current_artist = json_data["metadata"]["music"][0]["artists"][0]["name"]
            if current_music != music or current_artist != artist:
                music = current_music
                artist = current_artist
                external = json_data["metadata"]["music"][0]["external_metadata"]
                if "spotify" in external:
                    spotify_id = external["spotify"]["track"]["id"]
                    print("SPOT ID ", spotify_id)
                    if(token):
                        try:
                            r = sp.user_playlist_remove_all_occurrences_of_tracks(username,playlist,[spotify_id])
                            print(r)
                            r = sp.user_playlist_add_tracks(username, playlist, [spotify_id])
                            print(r)
                        except spotipy.client.SpotifyException:
                            print("exception")
                            refresh()
                            sp = spotipy.Spotify(auth=token)
                            sp.trace = False
                            sp.user_playlist_remove_all_occurrences_of_tracks(username,playlist,[spotify_id])
                            sp.user_playlist_add_tracks(username, playlist, [spotify_id])
        os.remove("/tmp/aaa.mp3")
        os.remove("/tmp/aaa.cue")

if __name__ == '__main__':
    refresh()
    main()