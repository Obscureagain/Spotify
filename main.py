import os
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import urllib.request
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

def main():
    image_url = spotify_image_url
    playlist_link = 'https://open.spotify.com/playlist/7cDPS2cPq8yot0ZwGMmuv4?si=bdc62e72451d4ba3'
    #print(full_playlist)
    #print(pd.value_counts(extract_artist(full_playlist)))
    full_playlist = get_playlist('spotify', get_playlist_id(playlist_link))
    
    create_artist_cloud(image_url, full_playlist)

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

def get_playlist_id(playlist_link):
    playlist_id = playlist_link.split("/")[-1].split("?")[0]
    return playlist_id

def get_playlist(username, playlist_id):
    r = sp.user_playlist_tracks(username, playlist_id)
    t = r['items']
    ids = []
    while r['next']:
        r = sp.next(r)
        t.extend(r['items'])
    for s in t: ids.append((s['track']['artists'][0]['name'], s['track']['name'], s['track']['id']))
    return ids

def extract_artist(lst):
    return [item[0] for item in lst]

def extract_song(lst):
    return [item[1] for item in lst]

#full_playlist = get_playlist('spotify', get_playlist_id(playlist_link))

# Set color palette based on a given image url

# Spotify pink/blue gradient image
spotify_image_url = 'https://www.freepnglogos.com/uploads/spotify-logo-png/spotify-icon-pink-logo-33.png'

# Python logo
python_image_url = 'https://cdn.freebiesupply.com/logos/large/2x/python-5-logo-png-transparent.png'

def get_colors(image_url, rgb1, rgb2):
    urllib.request.urlretrieve(image_url, "image.png")
    image = np.array(Image.open("image.png"))
    image_colors = ImageColorGenerator(image, default_color=None)
    image_mask = image.copy()
    image_mask[image_mask.sum(axis=2) == rgb1] = rgb2
    return image_colors, image_mask

# Create wordcloud from value counts of artist names
def create_artist_cloud(image_url, full_playlist):
    stopwords = ["feat"] + list(STOPWORDS)
    wc = WordCloud(stopwords=stopwords, background_color="white", max_words=None, mask=get_colors(image_url, 0, 255)[1]).generate_from_frequencies(pd.value_counts(extract_artist(full_playlist)))
    wc.recolor(color_func=get_colors(image_url, 0, 255)[0])
    plt.figure(figsize=(15,10))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    wc.to_file("wc_ArtistFrequencies.png")
    plt.show()

if __name__ == '__main__':
    main()