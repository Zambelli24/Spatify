from flask import Flask, request, Response
from spotify_connection import get_all_tracks, artist_search, related_artists
from math import ceil
from flask import render_template
import json


name_unfilled_response = "Name parameter not filled. Must provide '?artist=[artist name]' following query."

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/search_artist')
def search_for_artists():
    artist = request.args.get('artist')
    if artist is None:
        return Response("{}".format(name_unfilled_response), status=400)

    #return render_template('artist_search.html', artists=artist_search(artist))
    return Response(artist_search(artist), status=200)

@app.route('/track_search')
def track_search():
    artist = request.args.get('artist')
    if artist is None:
        return Response("{}".format(name_unfilled_response),
                        status=400)

    result = get_all_tracks.delay(artist)

    return Response(result.task_id, status=200)

@app.route('/track_search_status/<task_id>')
def get_status(task_id):
    celery_task = get_all_tracks.AsyncResult(task_id)
    if not celery_task.ready():
        return Response('Search Pending', status=202)
    else:
        return Response('Search is complete', status=200)


@app.route('/track_search_results/<task_id>', defaults={'page': 1})
@app.route('/track_search_results/<task_id>/<int:page>')
def show_results(task_id, page):
    celery_task = get_all_tracks.AsyncResult(task_id)

    if celery_task.get() == 'Artist name is not an exact match.':
        return Response(celery_task.get(), status=400)

    songs = json.loads(celery_task.get())

    pages = {}
    num_pages = ceil(len(songs['songs']) / 10)
    start_index = 0
    for index in range(1, num_pages+1):
        pages[index] = songs['songs'][start_index:index*10]
        start_index = index*10

    ret_songs = {"artist": songs['artist']}
    ret_songs["songs"] = pages[page]
    ret_songs["total_pages"] = num_pages
    ret_songs["current_page"] = page
    ret_songs["total_songs"] = len(songs['songs'])

    #return render_template('tracks.html', tracks=pages[page])
    return Response(json.dumps(ret_songs), status=200)


@app.route('/related_artists')
def get_related_artists():
    artist = request.args.get('artist')
    if artist is None:
        return Response("{}".format(name_unfilled_response),
                        status=400)

    #return render_template('related_artists.html', artist=(related_artists(artist)))
    if related_artists(artist) == 'Artist name is not an exact match.':
        return Response(related_artists(artist), status=400)

    return Response(related_artists(artist), status=200)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
