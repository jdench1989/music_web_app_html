class Album():
    def __init__(self, id, title, release_year, artist_id, artist):
        self.id = id
        self.title = title
        self.release_year = release_year
        self.artist_id = artist_id
        self.artist = artist

    def __repr__(self):
        return f"Album({self.id}, {self.title}, {self.release_year}, {self.artist_id}, {self.artist})"
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__