from lib.album import Album

def test_album_instantiates_with_correct_properties():
    """
    Test that an Album instance is created with the correct properties.

    This test verifies that when an Album object is instantiated with specific
    parameters, its attributes (id, title, release_year, and artist_id) are set
    correctly.

    Assertions:
        - The album's id should be 1.
        - The album's title should be "Test title".
        - The album's release_year should be 1999.
        - The album's artist_id should be 1.
    """
    album = Album(1, "Test title", 1999, 1)
    assert album.id == 1
    assert album.title == "Test title"
    assert album.release_year == 1999
    assert album.artist_id == 1

def test_albums_represented_nicely_as_strings():
    """
    Test that the Album object is represented correctly as a string.

    This test creates an Album instance with specific attributes and checks
    if its string representation matches the expected format.

    Assertions:
        str(album) == "Album(1, Test title, 1999, 1)"
    """
    album = Album(1, "Test title", 1999, 1)
    assert str(album) == "Album(1, Test title, 1999, 1)"

def test_albums_with_identical_properties_are_equal():
    """
    Test that two Album instances with identical properties are considered equal.

    This test creates two Album instances with the same ID, title, year, and artist ID,
    and asserts that they are considered equal using the equality operator.
    """
    album1 = Album(1, "Test title", 1999, 1)
    album2 = Album(1, "Test title", 1999, 1)
    assert album1 == album2