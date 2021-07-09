import datetime


class User:
    def __init__(self, user_id, name, user_type,
                 start_date_active=datetime.date.today(),
                 last_date_active=datetime.date.today()):
        self.user_id = user_id
        self.name = name
        self.start_date_active = start_date_active
        self.last_date_active = last_date_active
        self.user_type = user_type
