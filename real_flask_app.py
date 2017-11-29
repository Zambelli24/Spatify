from flask import Flask, request, Response, redirect, url_for
from spotify_connection import get_all_tracks, artist_search, related_artists
import time
import codecs
from math import ceil


name_unfilled_response = "Name parameter not filled. Must provide '?artist=[artist name]' following query."

app = Flask(__name__)


@app.route('/')
def homepage():
    f = codecs.open("ui.html", 'r')
    return f.read()


@app.route('/search_artist')
def search_for_artists():
    artist = request.args.get('artist')
    if artist is None:
        return Response("{}".format(name_unfilled_response), status=400)

    return str(artist_search(artist))


@app.route('/track_search')
def track_search():
    artist = request.args.get('artist')
    pending_artist = artist
    if artist is None:
        return Response("{}".format(name_unfilled_response),
                        status=400)

    result = get_all_tracks.delay(artist)

    return 'Song can be found at localhost:5000/track_search_results/{}'.format(result.task_id)

@app.route('/track_search_results/<task_id>', defaults={'page':1})
@app.route('/track_search_results/<task_id>/<int:page>')
def show_results(task_id, page):
    songs = get_all_tracks.AsyncResult(task_id).get(timeout=1)
    pages = {}
    num_pages = ceil(len(songs) / 10)
    start_index = 0
    for index in range(1, num_pages):
        pages[index] = songs[start_index:index*10]
        start_index = index*10
    if not page:
        return str(pages[1])
    return str(pages[page])


@app.route('/related_artists')
def get_related_artists():
    artist = request.args.get('artist')
    if artist is None:
        return Response("{}".format(name_unfilled_response),
                        status=400)

    return str(related_artists(artist))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
