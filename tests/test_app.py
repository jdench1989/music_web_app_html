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
        "Nina Simone",
        "Add a new artist"
    ])

def test_get_artist_by_id(db_connection, page, test_web_address):
    db_connection.seed("seeds/music_library.sql")
    page.goto(f"{test_web_address}/artists/1")
    h1_tag = page.locator("h1")
    expect(h1_tag).to_have_text("Pixies")
    p_tag = page.locator("p")
    expect(p_tag).to_have_text("Genre: Rock")
    
def test_create_artist(db_connection, page, test_web_address):
    db_connection.seed("seeds/music_library.sql")
    page.goto(f"http://{test_web_address}/artists")
    page.click("text=Add a new artist")
    page.fill("input[name='name']", "Adele")
    page.fill("input[name='genre']", "Pop")
    page.click("text=Create artist")
    title_element = page.locator(".t-title")
    expect(title_element).to_have_text("Adele")
    genre_element = page.locator(".t-genre")
    expect(genre_element).to_have_text("Genre: Pop")

def test_create_artist_error(db_connection, page, test_web_address):
    db_connection.seed("seeds/music_library.sql")
    page.goto(f"http://{test_web_address}/artists")
    page.click("text=Add a new artist")
    page.click("text=Create artist")
    errors = page.locator(".t-errors")
    expect(errors).to_have_text("There were errors with your submission: Name can't be blank, Genre can't be blank")