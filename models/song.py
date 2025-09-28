class Song:
    def __init__(self, title, artist, path):
        self.title = title
        self.artist = artist
        self.path = path

    def __str__(self):
        return f"{self.title} - {self.artist}"
