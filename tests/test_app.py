from playwright.sync_api import Page, expect

# Tests for your routes go here

def test_get_all_albums(db_connection, page, test_web_address):
    db_connection.seed("seeds/music_library.sql")
    page.goto(f"{test_web_address}/albums")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_have_text("Albums")
    h2_tags = page.locator("h2")
    expect(h2_tags).to_have_text([
        "Title: Doolittle",
        "Title: Surfer Rosa",
    ])
    p_tags = page.locator("p")
    expect(p_tags).to_have_text([
        "Released: 1989",
        "Released: 1988"
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
    h2_tags = page.locator("h2")
    expect(h2_tags).to_have_text([
        "Title: Doolittle",
        "Title: Surfer Rosa",
        "Title: Voyage"
    ])
    p_tags = page.locator("p")
    expect(p_tags).to_have_text([
        "Released: 1989",
        "Released: 1988",
        "Released: 2022"
    ])

def test_get_artists(db_connection, web_client):
    db_connection.seed("seeds/music_library.sql")
    response = web_client.get('/artists')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == "Pixies, ABBA, Taylor Swift, Nina Simone"

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
