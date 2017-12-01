import os
import unittest
import real_flask_app
import tempfile
from spotify_connection import app
import time
import json
from fakeredis import FakeRedis

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        r = FakeRedis()
        self.db_fd, real_flask_app.app.config['DATABASE'] = tempfile.mkstemp()
        real_flask_app.app.testing = True
        self.app = real_flask_app.app.test_client()
        #app.conf.update(CELERY_TASK_ALWAYS_EAGER=True)
        #app.conf.update(CELERY_REDIS_DB=r)
        #app.conf.update(CELERY_REDIS_HOST=r)
        #app.conf.update(CELERY_RESULT_BACKEND=r)
        #app.conf.update(CELERY_STATE_DB=r)

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(real_flask_app.app.config['DATABASE'])

    def test_homepage(self):
        homepage = self.app.get('/')
        assert b'Spatify API' in homepage.data

    def test_artist_search_no_artist(self):
        search = self.app.get('/search_artist')
        assert 400 == search.status_code

    def test_related_artists_no_artist(self):
        search = self.app.get('/related_artists')
        assert 400 == search.status_code

    def test_track_search_no_artist(self):
        search = self.app.get('/track_search')
        assert 400 == search.status_code

    def test_artist_search_no_matches(self):
        search = self.app.get('/search_artist?artist=eurhv')
        assert b'[]' in search.data

    def test_related_artists_bad_artist_name(self):
        search = self.app.get('/related_artists?artist=jim')
        assert 400 == search.status_code

    def test_track_search_bad_artist_name(self):
        search = self.app.get('/track_search?artist=joe')
        assert 200 == search.status_code
        time.sleep(5)
        search_url = '/track_search_status/' + search.data.decode('ascii')
        search2 = self.app.get(search_url)
        assert 200 == search2.status_code
        assert b'Search is complete' in search2.data
        final_url = '/track_search_results/' + search.data.decode('ascii')
        final_results = self.app.get(final_url)
        assert 400 == final_results.status_code
        assert b'Artist name is not an exact match.'

    def test_track_search_success(self):
        search = self.app.get('/track_search?artist=2Pac')
        search_url = '/track_search_status/' + search.data.decode('ascii')
        time.sleep(5)
        search2 = self.app.get(search_url)
        assert b'Search is complete' in search2.data
        search_url2 = '/track_search_results/' + search.data.decode('ascii')
        results = self.app.get(search_url2)
        final_results = json.loads(results.data)
        assert '2Pac' == final_results['artist']


    def test_track_search_results_not_ready(self):
        search = self.app.get('/track_search?artist=Eminem')
        search_url = '/track_search_status/' + search.data.decode('ascii')
        result_url = self.app.get(search_url)
        assert b'Search Pending' in result_url.data
        assert 202 == result_url.status_code

    def test_artist_search_success(self):
        search = self.app.get('/search_artist?artist=cupcakke')
        assert b'Cupcakke' in search.data
        assert b'cupcakKe' in search.data

    def test_related_artists_success(self):
        search = self.app.get('/related_artists?artist=50 Cent')
        results = json.loads(search.data)
        assert '50 Cent' == results['artist']
        assert 20 == len(results['results'])


if __name__ == '__main__':
    unittest.main()