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
        "Surfer Rosa by Pixies",
        "Add a new album"
    ])

def test_get_album_by_id(db_connection, page, test_web_address):
    db_connection.seed("seeds/music_library.sql")
    page.goto(f"{test_web_address}/albums/1")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_have_text("Doolittle")
    p_tags = page.locator("p")
    expect(p_tags).to_have_text([
        "Released: 1989",
        "Artist: Pixies"
        ])

def test_create_album(db_connection, page, test_web_address):
    db_connection.seed("seeds/music_library.sql")
    page.goto(f"http://{test_web_address}/albums")
    page.click("text=Add a new album")
    page.fill("input[name='title']", "Voyage")
    page.fill("input[name='release_year']", "2022")
    page.fill("input[name='artist_id']", "2")
    page.click("text=Create album")

    title_element = page.locator(".t-title")
    expect(title_element).to_have_text("Voyage")
    release_year_element = page.locator(".t-release-year")
    expect(release_year_element).to_have_text("Released: 2022")
    artist_element = page.locator(".t-artist")
    expect(artist_element).to_have_text("Artist: ABBA")

def test_create_album_error(db_connection, page, test_web_address):
    db_connection.seed("seeds/music_library.sql")
    page.goto(f"http://{test_web_address}/albums")
    page.click("text=Add a new album")
    page.click("text=Create album")
    errors = page.locator(".t-errors")
    expect(errors).to_have_text("There were errors with your submission: Title can't be blank, Release year can't be blank, Artist ID can't be blank")

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
