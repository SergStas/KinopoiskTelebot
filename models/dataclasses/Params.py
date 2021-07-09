class Params:
    def __init__(self, person=None, start_year=None, end_year=None, genres=None, threshold=None, rank=None,
                 actors_only=None, generate_gif=None, name=None, step=None):
        if genres is None:
            genres = []
        self.person = person
        self.start_year = start_year
        self.end_year = end_year
        self.genres = genres
        self.threshold = threshold
        self.rank = rank
        self.actors_only = actors_only
        self.generate_gif = generate_gif
        self.name = name
        self.step = step
