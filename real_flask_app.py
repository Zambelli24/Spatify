from flask import Flask, request, Response
from api_connection import Spotify_Connector

sc = Spotify_Connector()
name_unfilled_response = "Name parameter not filled. Must provide '?artist=[artist name]' following query."

app = Flask(__name__)


@app.route('/')
def homepage():
    return 'welcome to the api'


@app.route('/search_artist')
def artist_search():
    artist = request.args.get('artist')
    if artist is None:
        return Response("{}".format(name_unfilled_response), status=400)

    return str(sc.artist_search(artist))


@app.route('/track_search')
def track_search():
    artist = request.args.get('artist')
    if artist is None:
        return Response("{}".format(name_unfilled_response),
                        status=400)

    return str(sc.track_search(artist))


@app.route('/related_artists')
def related_artists():
    artist = request.args.get('artist')
    if artist is None:
        return Response("{}".format(name_unfilled_response),
                        status=400)

    return str(sc.related_artists(artist))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
