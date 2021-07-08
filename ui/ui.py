# TODO: Nikita 1170650256

import os
import re
import telebot
import asyncio
import datetime
from datetime import *
from enum import Enum, auto
from typing import AsyncContextManager
from telebot.apihelper import delete_message
from asyncio.subprocess import create_subprocess_shell

def stroke_pointer(stroke):
    return f"* {stroke}\n"
def stroke_sectioner(stroke):
    return f"{stroke}\n-----\n"

def user_mas_adder(bot,ids):
    name = "usu"
    count = 0
    for id in ids:
        session = Session(id,bot,f"{name}_{count}",False)
        count += 1


class User:
    def __init__(self,id,type,name):
        if type == "usu" or type == "adm" or type == "bos":
            self.id = id
            self.type = type
            self.name = name
            self.last_date_use = date.today()
            self.start_date_use = date.today()
        else:
            print("* err - Был указан несуществующий тип пользователя;")
class Parms:
    def __init__(self):
        self.name = None
        self.rank = None
        self.geners = None
        self.treshold = None
        self.end_year = None
        self.is_actors = None
        self.person_id = None
        self.start_year = None
        self.generate_gif = None
class Person:
    def __init__(self, person_id, person_type, full_name, positions, start_year, end_year, photo_url):
        self.person_id = person_id
        self.full_name = full_name
        self.positions = positions
        self.start_year = start_year
        self.end_year = end_year
        self.photo_url = photo_url
class Markups:
    def __init__(self):
        self.id = None
        self.body = None
        self.list = None
        self.index = None
class Session:
    count = 0
    bos_session = []
    adm_session = []
    usu_session = []
    bos_id_list = [632012083,1170650256]
    adm_id_list = [361877365,426134463,1839000131]
    def __init__(self,id,bot,name,intro):
        self.id = id
        self.bot = bot
        self.user = None
        self.store = []
        self.stage = None
        self.parms = Parms()
        self.target = None
        self.choosen = []
        self.messages = Messages(self)
        self.stage_path = []
        Session.count += 1
        stroke = ""
        for i in Session.bos_id_list:
            if i == id:
                self.user = User(id,"bos",name)
                Session.bos_session.append(self)
                stroke = "Добро пожаловать, уважаемый руководитель!"
        if self.user == None:
            for i in Session.adm_id_list:
                if i == id:
                    self.user = User(id,"adm",name)
                    Session.adm_session.append(self)
                    stroke = "Добро пожаловать, уважаемый администратор!"
        if self.user == None:
            self.user = User(id,"usu",name)
            Session.usu_session.append(self)
            stroke = "Добро пожаловать, уважаемый пользователь!"
        if intro:
            self.messages.other_message_sender(stroke)
            self.pauser()
            self.messages.help_geter()
            self.pauser()
            self.messages.func_geter()
    def finder(id):
        for i in Session.bos_session:
            if i.id == id:
                return i
        for i in Session.adm_session:
            if i.id == id:
                return i
        for i in Session.usu_session:
            if i.id == id:
                return i
    def pauser(self):
        asyncio.run(self.messages.pauser())
class Messages:
    row_date = 5
    row_list = 15
    column_date = 6
    year_begin = 1920

    def __init__(self,session):
        self.id = None
        self.info = []
        self.help = []
        self.index = None
        self.callback = None
        self.parms = Parms()
        self.markup = []
        self.session = session
        self.stage_list = []
        self.other_list = []
        self.target_list = []

    async def pauser(self):
        await asyncio.sleep(1)

    def clear(self):
        if self.id != None:
            self.message_deleter(self.id)
        help_clear()
        markup_clear()
    def all_clear(self):
        return None
    def help_clear(self):
        if len(self.help) > 0:
            for i in self.help:
                self.message_deleter(i)
        self.help.clear()
    def info_clear(self):
        if len(self.info) > 0:
            for i in self.info:
                self.message_deleter(i)
            self.info.clear()
    def parms_clear(self):
        self.session.parms = Parms()
    def markup_clear(self):
        if len(self.markup) > 0:
            for i in self.markup:
                self.message_deleter(i)
            self.markup.clear()
    def other_message_clear(self):
        for i in self.other_list:
            self.message_deleter(i)
        self.other_list.clear()
    def stage_message_clear(self):
        for i in self.stage_list:
            self.message_deleter(i)
        self.stage_list.clear()
    def target_message_clear(self):
        for i in self.target_list:
            self.message_deleter(i)
        self.target_list.clear()
    
    def id_geter(self):
        if self.id != None:
            self.message_deleter(self.id)
        self.id = self.message_sender(f"Ваш ID: {self.session.id};")
    def func_geter(self):
        self.markup_clear()
        self.markup.append(self.markup_sender("Какой функционал приложения вы желаете задействовать?",self.get_func_markuper()))
    def help_geter(self):
        self.help_clear()
        if self.session.user.type == "bos":
            self.help_message_sender(
                stroke_sectioner("Здесь вы можете ознакомиться со списком контрольных команд для данного бота:") +
                stroke_pointer("/id - Указывает Ваш ID в Телеграмме;") +
                stroke_pointer("/clear - Удаляет все сообщения бота;") +
                stroke_pointer("/fire_adm - Отнимает у указанного пользователя права администратора;") +
                stroke_pointer("/asign_adm - Наделяет указанного пользователя правами администратора;")
            )
            asyncio.run(self.pauser())
            self.help_message_sender(
                stroke_sectioner("Здесь вы можете получить дополнительные инструкии по использованию бота:") +
                stroke_pointer("Сделать пользователя администратором можно с помощью команды `assign_adm id` (где id - это ID пользователя в Телеграмме) или выбрав соответсвующий пункт в информации пользователя.") +
                stroke_pointer("Снять администратора с должности можно с помощью команды `fire_adm id` (где id - это ID пользователя в Телеграмме) или выбрав соответсвующий пункт в информации пользователя.")
            )
        if self.session.user.type == "adm":
            self.help_message_sender(
                stroke_sectioner("Здесь вы можете ознакомиться с полным списком команд, для продвинутого взаимодействия с ботом:") +
                stroke_pointer("/id - Получить Ваш ID в Телеграмме.") +
                stroke_pointer("/help - Получить список стандартных команд данного бота.") +
                stroke_pointer("/func - Получить перечень функций данного бота.") +
                stroke_pointer("/clear - Очистить все сообщения данного бота.") +
                stroke_pointer("/store - Получить Вашу историю запросов.") +
                stroke_pointer("/choosen - Получить список Ваших избранных запросов.") +
                stroke_pointer("/adm_help - Получить список административных команд для данного бота.") +
                stroke_pointer("/all_help - Получить полный список команд для данного бота.") +
                stroke_pointer("/get_users - Получить список пользователей.")
            )
    def store_geter(self):
        return None
    def users_geter(self):
        self.markup_clear()
        if len(Session.usu_session) > 0:
            self.markup.append(self.markup_sender("Список пользователей:",self.markup_list_geter(Session.usu_session,"usu")))
        else:
            self.other_message_sender("Список пользователей пуст!")
    def person_geter(self,id):
        person = None
        for i in person_list:
            if i.person_id == id:
                person = i
                break
        self.stage_list.append(self.photo_sender(person.photo_url))
        return self.message_sender(f"Годы деятельности: {person.start_year}-{person.end_year} Имя: {person.full_name};")
    def admins_geter(self):
        self.markup_clear()
        if len(Session.adm_session) > 0:
            self.markup.append(self.markup_sender("Список администраторов:",self.markup_list_geter(Session.adm_session,"adm")))
        else:
            self.other_message_sender("Список администраторов пуст!")
    def usu_info_geter(self,id):
        usu = Session.finder(id).user
        stroke = stroke_sectioner(f"выбран пользователь `{usu.name}`:")
        stroke += stroke_pointer(f"ID: {usu.id};")
        stroke += stroke_pointer(f"Имя: {usu.name};")
        stroke += stroke_pointer(f"Тип: {usu.type};")
        stroke += stroke_pointer(f"Дата регистрации: {usu.start_date_use};")
        stroke += stroke_pointer(f"Дата последней активности: {usu.last_date_use};")
        self.info_clear()
        if self.session.user.type == "adm":
            self.info_message_sender(stroke)
            return None
        if self.session.user.type == "bos":
            if usu.type == "usu":
                markup = self.markup_geter()
                markup.row(self.markup_button_geter("Выдать права администратора",f"assign_adm_{usu.id}"))
                self.info.append(self.markup_sender(stroke,markup))
                return None
            elif usu.type == "adm":
                markup = self.markup_geter()
                markup.row(self.markup_button_geter("Лишить прав администратора",f"fire_adm_{usu.id}"))
                self.info.append(self.markup_sender(stroke,markup))
    def markup_list_geter(self,arg_list,prefix):
        self.list = arg_list
        markup = self.markup_geter()
        arg_list_len = len(arg_list)
        if arg_list_len > 0:
            for i in range(self.index,self.index + Messages.row_list):
                text = ""
                callback = ""
                if i <= arg_list_len - 1:
                    if prefix == "usu":
                        text = f"№{'0' * (4 - len(str(i)))}{i} - Имя: {arg_list[i].user.name};"
                        callback = f"{prefix}_set_{Session.usu_session[i].id}"
                    elif prefix == "adm":
                        text = f"№{'0' * (4 - len(str(i)))}{i} - Имя: {arg_list[i].user.name};"
                        callback = f"{prefix}_set_{Session.adm_session[i].id}"
                else:
                    text = "-"
                    callback = "none"
                markup.row(self.markup_button_geter(text,callback))
            markup.row(
                self.markup_button_geter("⮝",f"{prefix}_up"),
                self.markup_button_geter("⮟",f"{prefix}_down")
            )
            return markup
    def markup_button_geter(self,text,callback):
        return telebot.types.InlineKeyboardButton(text=text,callback_data=callback)

    def adm_firer(self,id):
        session = Session.finder(id)
        Session.adm_session.remove(session)
        Session.usu_session.append(session)
        session.user.type = "usu"
        self.markup_clear()
        if len(Session.adm_session) > 0:
            self.admins_geter()
        self.usu_info_geter(id)
    def adm_assigner(self,id):
        session = Session.finder(id)
        Session.usu_session.remove(session)
        Session.adm_session.append(session)
        session.user.type = "adm"
        self.markup_clear()
        self.users_geter()
        self.usu_info_geter(id)

    def markup_geter(self):
        return telebot.types.InlineKeyboardMarkup()
    def markup_sender(self,text,markup):
        return self.session.bot.send_message(self.session.id,text,reply_markup=markup).id
    def markup_editer(self,text,markup):
        self.session.bot.edit_message_text(chat_id=self.session.id,message_id=self.markup[0],text=text,reply_markup=markup)
    def get_num_markuper(self):
        markup = Markups.get_markuper()
        markup.row(
            Markups.get_button_markuper("+10","add_10"),
            Markups.get_button_markuper("+5","add_5"),
            Markups.get_button_markuper("+1","add_1"),
            Markups.get_button_markuper("-1","inc_1"),
            Markups.get_button_markuper("-5","inc_5"),
            Markups.get_button_markuper("-10","inc_10")
        )
        markup.row(
            Markups.get_button_markuper("Принять","done")
        )
        return markup
    def get_func_markuper(self):
        markup = self.markup_geter()
        markup.row(self.markup_button_geter("Получить граф связей кино-персоны","graf"))
        markup.row(self.markup_button_geter("Получить хронологию кино-персоны","cron"))
        return markup
    def get_date_markuper(self):
        markup = Markups.get_markuper()
        for count1 in range(Markups.row_date):
            row = []
            count = 0
            for count2 in range(Markups.year_begin,Markups.year_begin + Markups.column_date):
                row.append(Markups.get_button_markuper(f"{count2}",f"set_{count2}"))
                count += 1
            markup.row().keyboard.append(row)
            self.index = Markups.year_begin
        markup.row(
            Markups.get_button_markuper("⮜","left"),
            Markups.get_button_markuper("⮞","right")
        )
        return markup
    def markup_list_changer(self,id,arg_list,prefix):
        self.usu_info_geter(id)
    def markup_list_rechanger(self,text,direct,arg_list,prefix):
        if direct == True:
            self.index -= Messages.row_list
            if self.index < 0:
                self.index += Messages.row_list
                return None
        else:
            self.index += Messages.row_list
            if len(arg_list) - 1 < self.index:
                self.index -= Messages.row_list
                return None
        markup = self.markup_list_geter(arg_list,prefix)
        self.markup_editer(text,markup)

    def photo_sender(self,url):
        return self.session.bot.send_photo(self.session.id,url).id
    def message_sender(self,text):
        return self.session.bot.send_message(self.session.id,text).id
    def message_deleter(self,id):
        self.session.bot.delete_message(self.session.id,id)
    def info_message_sender(self,text):
        self.info.append(self.message_sender(text))
    def help_message_sender(self,text):
        self.help.append(self.message_sender(text))
    def stage_massage_sender(self,text):
        self.stage_list.append(self.session.bot.send_message(self.session.id,text).id)
    def other_message_sender(self,text):
        self.other_list.append(self.session.bot.send_message(self.session.id,text).id)
    def target_message_sender(self,text):
        self.target_list.append(self.session.bot.send_message(self.session.id,text).id)

    def graf_targer(self,callback):
        self.callback = callback
        if self.session.target == None:
            self.parms_clear()
            self.markup_clear()
            self.session.stage_path = [
                Stage.typeSelect.value,
                Stage.nameSelect.value,
                Stage.idSelect.value,
                Stage.generSelect.value,
                Stage.rankSelect.value,
                Stage.thresholdSelect.value
            ]
            self.target_message_sender(stroke_pointer("Был указан функционал: построение графа;"))
            self.session.target = Target.graf.value
            self.session.parms.generate_gif = False
            self.session.stage = self.session.stage_path.pop(0)
            self.callback = "begin"
        if self.session.stage == Stage.typeSelect.value:
            self.type_supplicanter()
        if self.session.stage == Stage.nameSelect.value:
            self.name_supplicanter()
        if self.session.stage == Stage.idSelect.value:
            self.id_supplicanter()

    def type_supplicanter(self):
        if self.callback == "begin":
            self.markup_clear()
            markup = self.markup_geter()
            markup.row(
                self.markup_button_geter("Персонал","stf"),
                self.markup_button_geter("Актёр","act")
            )
            self.markup.append(self.markup_sender("Укажите тип кино-персоны, которую необходимо найти:",markup))
        if self.callback == "stf" or self.callback == "act":
            if self.callback == "stf":
                self.markup_clear()
                self.session.parms.is_actors = False
                self.target_message_sender(stroke_pointer("Был указан тип кино-персоны: персонал;"))
            elif self.callback == "act":
                self.markup_clear()
                self.session.parms.is_actors = True
                self.target_message_sender(stroke_pointer("Был указан тип кино-персоны: актёр;"))
            self.callback = "begin"
            self.session.stage = self.session.stage_path.pop(0)
    def name_supplicanter(self):
        if self.callback == "begin":
            self.session.pauser()
            self.stage_massage_sender("Укажите полное имя искомой персоны:")
        else:
            self.session.parms.person_id = []
            for i in person_list:
                if i.full_name == self.callback:
                    self.session.parms.person_id.append(i)
            len_list = len(self.session.parms.person_id)
            if len_list > 1:
                self.target_message_sender("Найдено множество соответсвий:")
                self.session.stage = self.session.stage_path.pop(0)
            elif len_list == 1:
                self.session.parms.person_id = self.session.parms.person_id[0]
                self.target_message_sender("Найдено однозначное соответствие:")
                self.session.stage_path.pop(0)
                self.session.stage = self.session.stage_path.pop(0)
                self.session.pauser()
                self.person_geter(self.session.parms.person_id.person_id)
                self.session.parms.person_id = self.session.parms.person_id.person_id
            elif len_list == 0:
                self.target_message_sender("Соответствий не найдено!")
                self.session.pauser()
                self.target_message_sender("Попробуйте повторить попытку.")
            self.callback = "begin"
    def id_supplicanter(self):
        if self.callback == "begin":
            self.session.pauser()
            for i in range(len(self.session.parms.person_id)):
                person = self.session.parms.person_id[i]
                markup = self.markup_geter()
                markup.row(self.markup_button_geter("Выбрать",f"set_pers_{person.person_id}"))
                self.stage_list.append(self.photo_sender(person.photo_url))
                self.markup.append(self.markup_sender(f"Годы деятельности: {person.start_year}-{person.end_year} Имя: {person.full_name};",markup))
        elif self.callback.find("set_pers") != -1:
            self.markup_clear()
            self.stage_message_clear()
            self.session.parms.person_id = self.session.parms.person_id[int(self.callback.split("_")[2])]
            person = self.session.parms.person_id
            self.session.parms.person_id = person.person_id
            self.target_message_sender(stroke_pointer("Была указана кино-персона:"))
            self.person_geter(person.person_id)
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

bot = telebot.TeleBot(os.environ["TOKEN"])

person_list = [
    Person(0,"act","Уилл Смит",0,1985,2021,"http://nightclick.ucoz.ru/_pu/9/s58863132.jpg"),
    Person(1,"act","Вин Дизель",1,1980,2021,"https://gif.cmtt.space/3/paper-media/7c/e9/70/8a6e9b24f617ad.jpg"),
    Person(2,"act","Скарлетт Йохансон",2,1920,2021,"https://i.pinimg.com/564x/c3/a6/a7/c3a6a7afed7067b05e4399e714e563c7.jpg"),
    Person(3,"act","Уилл Смит",3,1920,1977,"https://www.meme-arsenal.com/memes/259343770ad19e1dd9e5abd07e9d5b16.jpg")
]

testers_usu = [
    1170650255,
    1170650254,
    1170650253,
    1170650252,
    1170650251,
    1170650250,
    1170650249,
    1170650248,
    1170650247,
    1170650246,
    1170650245,
    1170650244,
    1170650243,
    1170650242,
    1170650241,
    1170650240,
    1170650239,
    1170650238,
    1170650237,
    1170650236,
    1170650235,
    1170650234,
    1170650233,
    1170650232,
    1170650231,
    1170650230
]
user_mas_adder(bot,testers_usu)

@bot.callback_query_handler(func=lambda call: True)
def call_determenant(call):
    id = call.message.chat.id
    text = call.data
    session = Session.finder(id)

    if session.target == Target.graf.value:
        session.messages.graf_targer(text)

    if text == "graf":
        session.messages.graf_targer(text)
    elif text == "usu_up":
        session.messages.markup_list_rechanger("Список пользователей:",True,Session.usu_session,"usu")
    elif text == "adm_up":
        session.messages.markup_list_rechanger("Список администратор:",True,Session.usu_session,"adm")
    elif text == "usu_down":
        session.messages.markup_list_rechanger("Список пользователей:",False,Session.usu_session,"usu")
    elif text == "adm_down":
        session.messages.markup_list_rechanger("Список администратор:",False,Session.usu_session,"adm")
    elif text.find("usu_set") != -1:
        session.messages.markup_list_changer(int(text.split("_")[2]),Session.usu_session,"usu")
    elif text.find("adm_set") != -1:
        session.messages.markup_list_changer(int(text.split("_")[2]),Session.adm_session,"adm")
    elif text.find("fire_adm") != -1:
        session.messages.adm_firer(int(text.split("_")[2]))
    elif text.find("assign_adm") != -1:
        session.messages.adm_assigner(int(text.split("_")[2]))
@bot.message_handler(commands=[
    "id",
    "func",
    "help",
    "clear",
    "get_users",
    "get_admins"])
def command_handler(message):
    id = message.chat.id
    text = message.text
    session = Session.finder(id)
    if session != None:
        if session.user.type != "usu":
            if text == "/get_users":
                session.messages.index = 0
                session.messages.users_geter()
            if session.user.type != "adm":
                if text == "/get_admins":
                    session.messages.index = 0
                    session.messages.admins_geter()
        if session.target != None:
            i = 0
        if text == "/id":
            session.messages.id_geter()
        if text == "/help":
            session.messages.help_geter()
        elif text == "/func":
            session.messages.func_geter()

    else:
        print ("GG")
@bot.message_handler(content_types=["text"])
def message_handler(message):
    id = message.chat.id
    text = message.text
    name = message.from_user.username
    session = Session.finder(id)
    if session != None:
        if session.target != None:
            if session.stage == Stage.nameSelect.value:
                session.messages.graf_targer(text)
    else:
        session = Session(id,bot,name,True)
    if message.text == "/test_date_markuper":
        markup = Markups()
        markup = markup.get_date_markuper()
        bot.send_message(message.chat.id,"test",reply_markup=markup)
    elif message.text == "/test_num_markuper":
        markup = Markups()
        bot.send_message(message.chat.id,"test",reply_markup=markup.get_num_markuper())
    elif message.text == "/test_list_markuper":
        markup = Markups()
        markup.index = 0
        bot.send_message(message.chat.id,"test",reply_markup=markup.get_list_markuper([1,2,5,16,20]))
bot.polling(none_stop=True)