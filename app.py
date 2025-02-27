from lib.album_repository import AlbumRepository
from lib.artist_repository import ArtistRepository
import os
from flask import Flask, request, render_template, Response
from lib.database_connection import get_flask_database_connection

# Create a new Flask app
app = Flask(__name__)

# == Your Routes Here ==
@app.route('/albums', methods=['GET'])
def get_all_albums():
    connection = get_flask_database_connection(app)
    repository = AlbumRepository(connection)
    albums = repository.all()
    return render_template("albums/index.html", albums=albums)

@app.route('/albums/<id>', methods=['GET'])
def get_album_by_id(id):
    connection = get_flask_database_connection(app)
    repository = AlbumRepository(connection)
    album = repository.find(id)
    return render_template("albums/album.html", album=album)

@app.route('/albums', methods=['POST'])
def create_album():
    if not all(key in request.form for key in ['title', 'release_year', 'artist_id']):
        return "Must include album title, release_year and artist id.", 400
    title = request.form['title']
    release_year = request.form['release_year']
    artist_id = request.form['artist_id']
    connection = get_flask_database_connection(app)
    repository = AlbumRepository(connection)
    repository.create(title, release_year, artist_id)
    return Response(status=200)

@app.route('/artists', methods=['GET'])
def get_all_artists():
    connection = get_flask_database_connection(app)
    repository = ArtistRepository(connection)
    artists = repository.all()
    return render_template("artists/index.html", artists=artists)

@app.route('/artists/<id>', methods=['GET'])
def get_artist_by_id(id):
    connection = get_flask_database_connection(app)
    repository = ArtistRepository(connection)
    artist = repository.find(id)
    return render_template("artists/artist.html", artist=artist)

@app.route('/artists', methods=["POST"])
def create_artist():
    if not all(key in request.form for key in ['name', 'genre']):
        return "Must include artist name and genre.", 400
    name = request.form['name']
    genre = request.form['genre']
    connection = get_flask_database_connection(app)
    repository = ArtistRepository(connection)
    repository.create(name, genre)
    return Response(status=200)


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
