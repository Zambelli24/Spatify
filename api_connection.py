import spotipy
import spotipy.util as util
import requests
import os


class Spotify_Connector:

	def __init__(self):
		client_id = os.environ['SPOTIFY_CLIENT_ID']
		client_secret = os.environ['SPOTIFY_CLIENT_SECRET']
		authorization_base_url = "https://accounts.spotify.com/authorize"
		token_url = 'https://accounts.spotify.com/api/token'
		redirect_uri = 'http://localhost:8888/callback'
		scope = 'user-library-read'
		username = os.environ['SPOTIFY_USERNAME']
		self.token = util.prompt_for_user_token(username,scope,client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri)

	def get_artist_ids(self, artist):
		url = 'https://api.spotify.com/v1/search?type=artist'
		header = {'Authorization': 'Bearer ' + self.token}
		r = requests.get(url, headers=header, params={'q': artist})
		data = r.json()['artists']['items']
		artist_list = {}
		for num in range(len(data)):
			artist_list[data[num]['name']] = data[num]['id']

		return artist_list

	def artist_search(self, artist):
		artist_list = self.get_artist_ids(artist)

		return list(artist_list.keys())

	def related_artists(self, artist):
		artist_ids = self.get_artist_ids(artist)

		url = 'https://api.spotify.com/v1/artists/{}/related-artists'.format(artist_ids.get(artist))
		header = {'Authorization': 'Bearer ' + self.token}
		r = requests.get(url, headers=header)
		r.raise_for_status()
		json_list = r.json()['artists']
		related_artists = []
		for num in range(len(json_list)):
			related_artists.append(json_list[num]['name'])
		return related_artists

	def track_search(self, artist):
		artist_ids = self.get_artist_ids(artist)
		albums = []
		url = 'https://api.spotify.com/v1/artists/{}/albums'.format(artist_ids.get(artist))
		header = {'Authorization': 'Bearer ' + self.token}
		r = requests.get(url, headers=header)
		r.raise_for_status()
		json_list = r.json()['items']
		for num in range(len(json_list)):
			albums.append(json_list[num]['id'])

		songs = []
		for code in albums:
			url = 'https://api.spotify.com/v1/albums/{}/tracks'.format(code)
			header = {'Authorization': 'Bearer ' + self.token}
			r = requests.get(url, headers=header)
			r.raise_for_status()
			json_list = r.json()['items']
			for num in range(len(json_list)):
				songs.append(json_list[num]['name'])
		print(songs)


