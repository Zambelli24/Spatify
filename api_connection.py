import spotipy
import spotipy.util as util
import requests
import os

client_id = os.environ['SPOTIFY_CLIENT_ID']
client_secret = os.environ['SPOTIFY_CLIENT_SECRET']

authorization_base_url = "https://accounts.spotify.com/authorize"
token_url = 'https://accounts.spotify.com/api/token'
#redirect_uri = 'http://localhost:8888/callback'
redirect_uri = 'http://localhost:5000/callback'

scope = 'user-library-read'
username = os.environ['SPOTIFY_USERNAME']

token = util.prompt_for_user_token(username,scope,client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri)
print(token)

#url = 'https://api.spotify.com/v1/artists/32vWCbZh0xZ4o9gkz4PsEU'

url = 'https://api.spotify.com/v1/search?type=artist'

header = {'Authorization': 'Bearer ' + token}

r = requests.get(url, headers=header, params={'q': 'Dolly Parton'})

print(r.json()['artists']['items'][0]['name'])

print(r.json()['artists']['items'][0]['id'])