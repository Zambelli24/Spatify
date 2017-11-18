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


