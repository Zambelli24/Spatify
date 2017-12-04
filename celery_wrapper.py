from spotify_connection import get_all_tracks, related_artists, artist_search

class Celery_Wrapper:

	def start_track_search_get_id(self, artist):
		return get_all_tracks.delay(artist).task_id

	def get_tracks_ready_status(self, task_id):
		return get_all_tracks.AsyncResult(task_id).ready()

	def get_all_tracks(self, task_id):
		return get_all_tracks.AsyncResult(task_id).get()

	def get_related_artists(self, artist):
		return related_artists(artist)

	def search_for_artist(self, artist):
		return artist_search(artist)