import os
import unittest
import real_flask_app
import tempfile
from spotify_connection import app

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, real_flask_app.app.config['DATABASE'] = tempfile.mkstemp()
        real_flask_app.app.testing = True
        self.app = real_flask_app.app.test_client()
        app.conf.update(CELERY_TASK_ALWAYS_EAGER=True)

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

    def test_track_search_results_not_ready(self):
        search = self.app.get('/track_search?artist=Eminem')
        result_url = self.app.get(search.data)
        assert b'Search Pending' in result_url.data


if __name__ == '__main__':
    unittest.main()