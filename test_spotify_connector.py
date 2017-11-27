from unittest import TestCase

from api_connection import Spotify_Connector
from spotify_connection import get_all_tracks, artist_search, related_artists


class TestSpotifyConnector(TestCase):

	def test_artist_search_no_matches(self):
		artists = artist_search('reaknsvl')
		self.assertEqual(0, len(artists))
		self.assertEqual([], artists)

	def test_related_artists_no_matches(self):
		self.assertRaises(Exception, related_artists, 'acsnjr')

	def test_artist_search_small_list(self):
		artists = artist_search('cupcakke')
		self.assertEqual(2, len(artists))
		self.assertEqual(['cupcakKe', 'Cupcakke'], artists)

	def test_related_artists_small_list(self):
		artists = related_artists('Katy Perry')
		self.assertEqual(20, len(artists))

	def test_track_search_artist_with_few_songs(self):
		tracks = get_all_tracks('Cupcakke')
		self.assertEqual(1, len(tracks))

	def test_track_search_not_real_artist(self):
		self.assertRaises(Exception, get_all_tracks, 'neibvh')