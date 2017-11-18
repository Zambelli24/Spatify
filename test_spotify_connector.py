from unittest import TestCase

from api_connection import Spotify_Connector

class TestSpotifyConnector(TestCase):

	def test_artist_search(self):
		sc = Spotify_Connector()
		artists = sc.artist_search('reaknsvl')
		self.assertEqual(0, len(artists))
		self.assertEqual([], artists)
