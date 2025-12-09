class Movie:
    def __init__(self, id, title, genre, duration, rating, imdb_rating, description, poster_path, tagline, cast, director):
        self.id = id
        self.title = title
        self.genre = genre
        self.duration = duration
        self.rating = rating # MPAA
        self.imdb_rating = imdb_rating # Stars
        self.description = description
        self.poster_path = poster_path
        self.tagline = tagline
        self.cast = cast
        self.director = director

    def get_display_duration(self):
        # Centralized Logic: Converts minutes to "Xh Ym"
        try:
            mins = int(self.duration)
            h = mins // 60
            m = mins % 60
            return f"{h}h {m}m"
        except:
            return "0h 0m"

    def get_poster_path(self):
        import os
        if not self.poster_path: return "assets/sample_posters/default.png"
        if os.path.exists(self.poster_path): return self.poster_path
        return "assets/sample_posters/default.png"