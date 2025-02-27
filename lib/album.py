class Album():
    def __init__(self, id, title, release_year, artist_id, artist=None):
        self.id = id
        self.title = title
        self.release_year = release_year
        self.artist_id = artist_id
        self.artist = artist

    def __repr__(self):
        return f"Album({self.id}, {self.title}, {self.release_year}, {self.artist_id}, {self.artist})"
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def is_valid(self):
        if not all([self.title, self.release_year, self.artist_id]):
            return False
        else:
            return True
        
    def generate_errors(self):
        errors = []
        if self.title == None or self.title == "":
            errors.append("Title can't be blank")
        if self.release_year == None or self.release_year == "":
            errors.append("Release year can't be blank")
        if self.artist_id == None or self.artist_id == "":
            errors.append("Artist ID can't be blank")
        if len(errors) == 0:
            return None
        else:
            return ", ".join(errors)