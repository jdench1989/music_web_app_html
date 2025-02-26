from playwright.sync_api import Page, expect

# Tests for your routes go here

def test_get_all_albums(db_connection, web_client):
    db_connection.seed("seeds/music_library.sql")
    response = web_client.get('/albums')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == "" \
        "Album(1, Doolittle, 1989, 1)\n" \
        "Album(2, Surfer Rosa, 1988, 1)\n" \
        "Album(3, Waterloo, 1974, 2)\n" \
        "Album(4, Super Trouper, 1980, 2)\n" \
        "Album(5, Bossanova, 1990, 1)\n" \
        "Album(6, Lover, 2019, 3)\n" \
        "Album(7, Folklore, 2020, 3)\n" \
        "Album(8, I Put a Spell on You, 1965, 4)\n" \
        "Album(9, Baltimore, 1978, 4)\n" \
        "Album(10, Here Comes the Sun, 1971, 4)\n" \
        "Album(11, Fodder on My Wings, 1982, 4)\n" \
        "Album(12, Ring Ring, 1973, 2)" 

def test_post_albums_any_fields_missing(db_connection, web_client):
    db_connection.seed("seeds/music_library.sql")
    response = web_client.post('/albums')
    assert response.status_code == 400
    assert response.data.decode('utf-8') == "Must include album title, release_year and artist id."
    
    response = web_client.post('/albums', data={"title": "Voyage", "release_year": "2022"})
    assert response.status_code == 400
    assert response.data.decode('utf-8') == "Must include album title, release_year and artist id."
    
    response = web_client.post('/albums', data={"release_year": "2022", "artist_id": "2"})
    assert response.status_code == 400
    assert response.data.decode('utf-8') == "Must include album title, release_year and artist id."
    
    response = web_client.post('/albums', data={"title": "Voyage", "artist_id": "2"})
    assert response.status_code == 400
    assert response.data.decode('utf-8') == "Must include album title, release_year and artist id."

"""
POST /albums
Parameters:
    title: Voyage
    release_year: 2022
    artist_id: 2
Expected response (200 OK)
"""
def test_post_albums_valid_entry(db_connection, web_client):
    db_connection.seed("seeds/music_library.sql")
    post_response = web_client.post('/albums', data={
        "title": "Voyage", 
        "release_year": '2022', 
        "artist_id": '2'
    })
    assert post_response.status_code == 200
    assert post_response.data.decode('utf-8') == ""
    get_response = web_client.get('/albums')
    assert get_response.data.decode('utf-8') == "" \
        "Album(1, Doolittle, 1989, 1)\n" \
        "Album(2, Surfer Rosa, 1988, 1)\n" \
        "Album(3, Waterloo, 1974, 2)\n" \
        "Album(4, Super Trouper, 1980, 2)\n" \
        "Album(5, Bossanova, 1990, 1)\n" \
        "Album(6, Lover, 2019, 3)\n" \
        "Album(7, Folklore, 2020, 3)\n" \
        "Album(8, I Put a Spell on You, 1965, 4)\n" \
        "Album(9, Baltimore, 1978, 4)\n" \
        "Album(10, Here Comes the Sun, 1971, 4)\n" \
        "Album(11, Fodder on My Wings, 1982, 4)\n" \
        "Album(12, Ring Ring, 1973, 2)\n" \
        "Album(13, Voyage, 2022, 2)"
        
def test_get_artists(db_connection, web_client):
    db_connection.seed("seeds/music_library.sql")
    response = web_client.get('/artists')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == "Pixies, ABBA, Taylor Swift, Nina Simone"

"""
when we run a POST to /artists
with a new artist
then we expect a 200 response
AND we expect the artist to be added to the database
"""
def test_add_artist(db_connection, web_client):
    db_connection.seed("seeds/music_library.sql")
    post_response = web_client.post('/artists', data={'name' : 'BeeJees', 'genre': 'Funk'})
    get_response = web_client.get('/artists')
    assert post_response.status_code == 200
    assert post_response.data.decode('utf-8') == ''
    assert get_response.status_code == 200
    assert get_response.data.decode('utf-8') == "Pixies, ABBA, Taylor Swift, Nina Simone, BeeJees"

def test_add_artists_any_fields_missing(db_connection, web_client):
    db_connection.seed("seeds/music_library.sql")
    response = web_client.post('/artists')
    assert response.status_code == 400
    assert response.data.decode('utf-8') == "Must include artist name and genre."
    response = web_client.post('/artists', data={"name": "The Beatles"})
    assert response.status_code == 400
    assert response.data.decode('utf-8') == "Must include artist name and genre."
    
    response = web_client.post('/artists', data={"genre": "Rock"})
    assert response.status_code == 400
    assert response.data.decode('utf-8') == "Must include artist name and genre."
