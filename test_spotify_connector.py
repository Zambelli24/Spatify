from unittest import TestCase
import json

from spotify_connection import get_all_tracks, artist_search, related_artists


class TestSpotifyConnector(TestCase):

	def test_artist_search_no_matches(self):
		artists = json.loads(artist_search('reaknsvl'))
		self.assertEqual(0, len(artists['results']))
		self.assertEqual('reaknsvl', artists['artist'])
		self.assertEqual([], artists['results'])

	def test_related_artists_no_matches(self):
		artists = related_artists('acsnjr')
		self.assertEqual('Artist name is not an exact match.', artists)

	def test_artist_search_small_list(self):
		artists = json.loads(artist_search('cupcakke'))
		self.assertEqual(2, len(artists['results']))
		self.assertEqual('cupcakke', artists['artist'])
		self.assertEqual(['cupcakKe', 'Cupcakke'], artists['results'])

	def test_related_artists_small_list(self):
		artists = json.loads(related_artists('Katy Perry'))
		self.assertEqual('Katy Perry', artists['artist'])
		self.assertEqual(20, len(artists['results']))

	def test_track_search_artist_with_few_songs(self):
		tracks = json.loads(get_all_tracks('Cupcakke'))
		self.assertEqual('Cupcakke', tracks['artist'])
		self.assertEqual(1, len(tracks['songs']))

	def test_track_search_not_real_artist(self):
		tracks = get_all_tracks('neibvh')
		self.assertEqual('Artist name is not an exact match.', tracks)

	def test_artist_search_with_spaces(self):
		artists = json.loads(artist_search('twenty+one+pilots'))
		self.assertEqual(1, len(artists['results']))
		self.assertEqual('twenty+one+pilots', artists['artist'])
		self.assertEqual(['Twenty One Pilots'], artists['results'])

	def test_related_artists_with_spaces(self):
		artists = json.loads(related_artists('Fall Out Boy'))
		self.assertEqual('Fall Out Boy', artists['artist'])
		self.assertEqual(20, len(artists['results']))

	def test_track_search_with_spaces(self):
		tracks = json.loads(get_all_tracks("My Chemical Romance"))
		self.assertEqual('My Chemical Romance', tracks['artist'])
		self.assertEqual(181, len(tracks['songs']))
