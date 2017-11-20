from unittest import TestCase

from api_connection import Spotify_Connector

class TestSpotifyConnector(TestCase):

	def test_artist_search_no_matches(self):
		sc = Spotify_Connector()
		artists = sc.artist_search('reaknsvl')
		self.assertEqual(0, len(artists))
		self.assertEqual([], artists)

	def test_related_artists_no_matches(self):
		sc = Spotify_Connector()
		self.assertRaises(Exception, sc.related_artists, 'acsnjr')

	def test_artist_search_small_list(self):
		sc = Spotify_Connector()
		artists = sc.artist_search('cupcakke')
		self.assertEqual(2, len(artists))
		self.assertEqual(['cupcakKe', 'Cupcakke'], artists)

	def test_related_artists_small_list(self):
		sc = Spotify_Connector()
		artists = sc.related_artists('Katy Perry')
		self.assertEqual(20, len(artists))

	def test_track_search_artist_with_few_songs(self):
		sc = Spotify_Connector()
		tracks = sc.track_search('Cupcakke')
		self.assertEqual(1, len(tracks))