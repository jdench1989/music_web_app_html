from lib.album_repository import AlbumRepository
from lib.album import Album

"""
When we call AlbumRepository.all()
We get a list containing Album objects correctly representing the seed data
"""
def test_get_all_albums(db_connection):
    db_connection.seed("seeds/music_library.sql")
    repository = AlbumRepository(db_connection)
    albums = repository.all()
    assert albums == [
        Album(1, "Doolittle", 1989, 1),
        Album(2, "Surfer Rosa", 1988, 1),
        Album(3, "Waterloo", 1974, 2),
        Album(4, "Super Trouper", 1980, 2),
        Album(5, "Bossanova", 1990, 1),
        Album(6, "Lover", 2019, 3),
        Album(7, "Folklore", 2020, 3),
        Album(8, "I Put a Spell on You", 1965, 4),
        Album(9, "Baltimore", 1978, 4),
        Album(10, "Here Comes the Sun", 1971, 4),
        Album(11, "Fodder on My Wings", 1982, 4),
        Album(12, "Ring Ring", 1973, 2)
    ]

"""
When we call AlbumRepository.find(album_id)
We get a single Album object returned matching the album_id argument
"""
def test_find_single_album_by_id(db_connection):
    db_connection.seed("seeds/music_library.sql")
    repository = AlbumRepository(db_connection)
    album_1 = repository.find(1)
    assert album_1 == Album(1, "Doolittle", 1989, 1)

"""
When we call AlbumRepository.create()
A new album is added to the database
"""
def test_create_method_adds_record_to_dataabse(db_connection):
    db_connection.seed("seeds/music_library.sql")
    repository = AlbumRepository(db_connection)
    repository.create("Voyage", 2021, 2)
    albums = repository.all()
    assert len(albums) == 13
    assert albums[-1].title == "Voyage"

"""
When we call AlbumRepository.delete()
The album is deleted
"""
def test_delete_method(db_connection):
    db_connection.seed("seeds/music_library.sql")
    repository = AlbumRepository(db_connection)
    repository.delete(1)
    albums = repository.all()
    assert len(albums) == 11
    assert Album(1, "Doolittle", 1989, 1) not in albums