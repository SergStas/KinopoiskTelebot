import datetime
from datetime import *
from enum import Enum, auto

class User:
    def __init__(self,id,name):
        self.id = id
        self.type = "usu"
        self.name = name
        self.date_last = date.today()
        self.date_start = date.today()
class Person:
    def __init__(self, person_id, type, full_name, positions, start_year, end_year,photo):
        self.type = type
        self.photo = photo
        self.end_year = end_year
        self.person_id = person_id
        self.full_name = full_name
        self.positions = positions
        self.start_year = start_year
class Select:
    def __init__(self):
        self.rank = None
        self.type = None
        self.step = None
        self.stage = None
        self.gener = []
        self.target = None
        self.person = None
        self.end_date = None
        self.treshold = None
        self.start_date = None
        self.stage_complete = []
        self.message_select = None
class Markup:
    def __init__(self):
        self.id = None
        self.type = None
        self.index = None
        self.markup = None
        self.mas_data = None
        self.first_date = None
        self.markup_selector = []
class Session:
    def __init__(self,id,bot,username):
        self.id = id
        self.bot = bot
        self.select_num = 0
        self.choose_store = []
        self.selects_store = []
        self.user = User(id,username)
        self.select = Select()
        self.bot_talk = False
        self.message_id = None
        self.messages_id = []
        self.message_info = None
        self.message_help = None
        self.message_markup = Markup()
        self.stage_messages_id = []
class User_store:
    def __init__(self,id,selects,choosen_selects):
        self.id = id
        self.selects = selects,
        self.choosen_selects = choosen_selects

class Stage(Enum):
    result = auto()
    idSelect = auto()
    rankSelect = auto()
    typeSelect = auto()
    nameSelect = auto()
    stepSelect = auto()
    generSelect = auto()
    endYearSelect = auto()
    thresholdSelect = auto()
    startYearSelect = auto()
class Gener(Enum):
    Нуар = auto()
    Экшен = auto()
    Ужасы = auto()
    Драма = auto()
    Слэшер = auto()
    Боевик = auto()
    Мюзикл = auto()
    Фэнтези = auto()
    Военный = auto()
    Комедия = auto()
    Вестерн = auto()
    Детский = auto()
    Криминал = auto()
    Детектив = auto()
    Семейный = auto()
    Мелодрама = auto()
    Биография = auto()
    Фантастика = auto()
    Мультфильм = auto()
    Спортивный = auto()
    Исторический = auto()
    Приключенческий = auto()
class Target(Enum):
    graf = auto()
    cron = auto()
    persons = auto()
    person_films = auto()
