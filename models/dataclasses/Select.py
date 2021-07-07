class Select:
    def __init__(self, threshold, target):
        self.rank = None
        self.type = None
        self.step = None
        self.stage = None
        self.genre = []
        self.target = target
        self.person = None
        self.end_date = None
        self.threshold = threshold
        self.start_date = None
        self.stage_complete = []
        self.message_select = None