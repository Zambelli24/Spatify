import spotipy
import spotipy.util as util
import requests
import os
from celery import Celery
import json

client_id = os.environ['SPOTIFY_CLIENT_ID']
client_secret = os.environ['SPOTIFY_CLIENT_SECRET']
authorization_base_url = "https://accounts.spotify.com/authorize"
token_url = 'https://accounts.spotify.com/api/token'
redirect_uri = 'http://localhost:8888/callback'
scope = 'user-library-read'
username = os.environ['SPOTIFY_USERNAME']

token = util.prompt_for_user_token(username,scope,client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri)

app = Celery('spotify_connection', backend='redis://localhost:6379', broker='redis://localhost')

def get_artist_ids(artist):
	url = 'https://api.spotify.com/v1/search?type=artist'
	header = {'Authorization': 'Bearer ' + token}
	r = requests.get(url, headers=header, params={'q': artist})
	data = r.json()['artists']['items']
	artist_list = {}
	for num in range(len(data)):
		artist_list[data[num]['name']] = data[num]['id']

	return artist_list

def artist_search(artist):
	artist_list = get_artist_ids(artist)

	artists = {'artist': artist, 'results': list(artist_list.keys())}

	return json.dumps(artists)

def related_artists(artist):
	artist_ids = get_artist_ids(artist)

	url = 'https://api.spotify.com/v1/artists/{}/related-artists'.format(artist_ids.get(artist))
	header = {'Authorization': 'Bearer ' + token}
	r = requests.get(url, headers=header)
	if r.status_code != 200:
		return "Artist name is not an exact match."
	json_list = r.json()['artists']
	artists = []

	for num in range(len(json_list)):
		artists.append(json_list[num]['name'])
	related_artists = {'artist': artist, 'results': artists}

	return json.dumps(related_artists)

@app.task
def get_all_tracks(artist):
	artist_ids = get_artist_ids(artist)
	albums = []
	url = 'https://api.spotify.com/v1/artists/{}/albums'.format(artist_ids.get(artist))
	header = {'Authorization': 'Bearer ' + token}
	r = requests.get(url, headers=header)
	if r.status_code != 200:
		return "Artist name is not an exact match."
	json_list = r.json()['items']
	for num in range(len(json_list)):
		albums.append(json_list[num]['id'])

	songs = []
	for code in albums:
		url = 'https://api.spotify.com/v1/albums/{}/tracks'.format(code)
		header = {'Authorization': 'Bearer ' + token}
		r = requests.get(url, headers=header)
		r.raise_for_status()
		json_list = r.json()['items']
		for num in range(len(json_list)):
			songs.append(json_list[num]['name'])
	track_info = {'artist': artist, 'songs': songs}
	return json.dumps(track_info)

