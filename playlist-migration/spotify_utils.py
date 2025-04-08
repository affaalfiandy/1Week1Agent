import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8080"),
    scope="playlist-read-private playlist-modify-public playlist-modify-private",
))


def extract_playlist(link: str):
    playlist_id = link.split("/playlist/")[-1].split("?")[0]
    results = sp.playlist_tracks(playlist_id)
    tracks = results["items"]

    songs = []
    for item in tracks:
        track = item["track"]
        title = track["name"]
        artist = track["artists"][0]["name"]
        songs.append({"title": title, "artist": artist})
    return songs
