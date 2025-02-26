from lib.album import Album

class AlbumRepository():

    def __init__(self, connection):
        self._connection = connection
    
    def all(self):
        rows = self._connection.execute("SELECT * FROM albums")
        albums = []
        for row in rows:
            album = Album(row["id"], row["title"], row["release_year"], row["artist_id"])
            albums.append(album)
        return albums
    
    def find(self, album_id):
        row = self._connection.execute("SELECT * FROM albums WHERE id = %s", [album_id])
        album = Album(row[0]["id"], row[0]["title"], row[0]["release_year"], row[0]["artist_id"])
        return album
    
    def create(self, title, release_year, artist_id):
        self._connection.execute("INSERT INTO albums (title, release_year, artist_id) VALUES (%s, %s, %s)", [title, release_year, artist_id])

    def delete(self, album_id):
        self._connection.execute("DELETE FROM albums WHERE id = %s", [album_id])