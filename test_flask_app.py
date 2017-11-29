import os
import unittest
import real_flask_app
import tempfile

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, real_flask_app.app.config['DATABASE'] = tempfile.mkstemp()
        real_flask_app.app.testing = True
        self.app = real_flask_app.app.test_client()

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


if __name__ == '__main__':
    unittest.main()