import os
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# Get Spotify API key and secret 

def read_secrets() -> dict:
    filename = os.path.join('secrets.json')
    try:
        with open(filename, mode='r') as f:
            return json.loads(f.read())
    except FileNotFoundError:
        return {}
secrets = read_secrets()

# Spotify credentials manager
client_credentials_manager = SpotifyClientCredentials(client_id=secrets['CLIENT_ID'], client_secret=secrets['CLIENT_SECRET'])
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)