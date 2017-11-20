from flask import Flask, request, Response
from api_connection import Spotify_Connector

sc = Spotify_Connector()

app = Flask(__name__)


@app.route('/search_artist')
def artist_search():
    artist = request.args.get('artist')
    if artist is None:
        return Response("Name parameter not fulfilled.", status=400)

    return str(sc.artist_search(artist))


@app.route('/track_search')
def track_search():
    artist = request.args.get('artist')
    if artist is None:
        return Response("Name parameter not fulfilled.", status=400)
    return str(sc.track_search(artist))


@app.route('/related_artists')
def related_artists():
    artist = request.args.get('artist')
    if artist is None:
        return Response("Name parameter not fulfilled.", status=400)

    return str(sc.related_artists(artist))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
