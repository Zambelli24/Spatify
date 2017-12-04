from spotify_connection import related_artists, artist_search
import json

class Mock_Celery_Wrapper:

	def __init__(self):
		self.artists = ['Eminem', '2Pac']
		self.ready = False
		self.return_value = ''
		self.eminem_info = json.dumps({'artist': 'Eminem', 'songs': ['The Real Slim Shady']})
		self.pac_info = json.dumps({'artist': '2Pac', 'songs': ['Thugz Mansion']})
		self.bob_info = json.dumps({'artist': 'Bob', 'songs': ['001', '002', '003', '004', '005', '006', '007', '008', '009', '010', '011']})
		self.em_task_id = '3892752'
		self.pac_task_id = '93478854'
		self.bob_task_id = '30942758'

	def start_track_search_get_id(self, artist):
		if artist not in self.artists:
			self.return_value = 'Artist name is not an exact match.'

		if artist == 'Eminem':
			return self.em_task_id
		elif artist == '2Pac':
			return self.pac_task_id
		elif artist == 'Bob':
			return self.bob_task_id
		else:
			return '12345678'

	def get_tracks_ready_status(self, task_id):
		return self.ready

	def get_all_tracks(self, task_id):
		if task_id == self.em_task_id:
			return self.eminem_info
		elif task_id == self.pac_task_id:
			return self.pac_info
		elif task_id == self.bob_task_id:
			return self.bob_info
		else:
			return self.return_value

	def get_related_artists(self, artist):
		names = ['Eminem', '2Pac', 'Dr. Dre']
		if artist == '50 Cent':
			ret_obj = {'artist': '50 Cent', 'results': names}
			return json.dumps(ret_obj)
		else:
			return json.dumps([])

	def search_for_artist(self, artist):
		names = ['Cupcakke', 'cupcakKe']
		if artist == 'cupcakke':
			ret_obj = {'artist': 'cupcakke', 'results': names}
			return json.dumps(ret_obj)
		else:
			return json.dumps([])

	def change_ready_status(self):
		self.ready = True
