from lib.album import Album

class AlbumRepository():

    def __init__(self, connection):
        self._connection = connection
    
    def all(self):
        rows = self._connection.execute(
            "SELECT " \
                "al.id, " \
                "title, " \
                "release_year, " \
                "artist_id, " \
                "name as artist "\
            "FROM albums al " \
            "JOIN artists ar ON al.artist_id = ar.id"
            )
        albums = []
        for row in rows:
            album = Album(row["id"], row["title"], row["release_year"], row["artist_id"], row["artist"])
            albums.append(album)
        return albums
    
    def find(self, album_id):
        row = self._connection.execute(
            "SELECT " \
                "al.id, " \
                "title, " \
                "release_year, " \
                "artist_id, " \
                "name as artist "\
            "FROM albums al " \
            "JOIN artists ar ON al.artist_id = ar.id " \
            "WHERE al.id = %s", [album_id])
        album = Album(row[0]["id"], row[0]["title"], row[0]["release_year"], row[0]["artist_id"], row[0]["artist"])
        return album
    
    def create(self, album):
        rows = self._connection.execute("INSERT INTO albums (title, release_year, artist_id) VALUES (%s, %s, %s) RETURNING id", [album.title, album.release_year, album.artist_id])
        row = rows[0]
        album.id = row['id']
        return album

    def delete(self, album_id):
        self._connection.execute("DELETE FROM albums WHERE id = %s", [album_id])