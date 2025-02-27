from playwright.sync_api import Page, expect

# Tests for your routes go here

def test_get_all_albums(db_connection, page, test_web_address):
    db_connection.seed("seeds/music_library.sql")
    page.goto(f"{test_web_address}/albums")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_have_text("Albums")
    a_tags = page.locator("a")
    expect(a_tags).to_have_text([
        "Doolittle by Pixies",
        "Surfer Rosa by Pixies"
    ])

def test_get_album_by_id(db_connection, page, test_web_address):
    db_connection.seed("seeds/music_library.sql")
    page.goto(f"{test_web_address}/albums/1")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_have_text("Doolittle")
    p_tag = page.locator("p")
    expect(p_tag).to_have_text("Released: 1989\nArtist: Pixies")
    
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

def test_post_albums_valid_entry(db_connection, web_client, page, test_web_address):
    db_connection.seed("seeds/music_library.sql")
    post_response = web_client.post('/albums', data={
        "title": "Voyage", 
        "release_year": '2022', 
        "artist_id": '2'
    })
    assert post_response.status_code == 200
    assert post_response.data.decode('utf-8') == ""
    page.goto(f"{test_web_address}/albums")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_have_text("Albums")
    a_tags = page.locator("a")
    expect(a_tags).to_have_text([
        "Doolittle by Pixies",
        "Surfer Rosa by Pixies",
        "Voyage by ABBA"
    ])

def test_get_all_artists(db_connection, page, test_web_address):
    db_connection.seed("seeds/music_library.sql")
    page.goto(f"{test_web_address}/artists")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_have_text("Artists")
    a_tags = page.locator("a")
    expect(a_tags).to_have_text([
        "Pixies",
        "ABBA",
        "Taylor Swift",
        "Nina Simone"
    ])

def test_get_artist_by_id(db_connection, page, test_web_address):
    db_connection.seed("seeds/music_library.sql")
    page.goto(f"{test_web_address}/artists/1")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_have_text("Pixies")
    p_tag = page.locator("p")
    expect(p_tag).to_have_text("Genre: Rock")
    
def test_add_artist(db_connection, web_client, page, test_web_address):
    db_connection.seed("seeds/music_library.sql")
    post_response = web_client.post('/artists', data={'name' : 'Bee Gees', 'genre': 'Funk'})
    assert post_response.status_code == 200
    assert post_response.data.decode('utf-8') == ''
    page.goto(f"{test_web_address}/artists")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_have_text("Artists")
    a_tags = page.locator("a")
    expect(a_tags).to_have_text([
        "Pixies",
        "ABBA",
        "Taylor Swift",
        "Nina Simone",
        "Bee Gees"
    ])

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
