# TODO: Nikita

import os
from typing import AsyncContextManager
import telebot
import asyncio
from telebot.apihelper import delete_message

from enum import Enum

class Stage(Enum):
    nameSelect = 0
    idSelect = 1
    generSelect = 2
    thresholdSelect = 3
    rankSelect = 4
    startYearSelect = 5
    endYearSelect = 6
    res = 7
class Target(Enum):
    graf = 0,
    cron = 1,
    persons = 2,
    person_films = 3
class Genre(Enum):
    any = 0
    action = 1
    slasher = 2
    thriller = 3
    military = 4
    horror = 5
    fiction = 6
    fantasy = 7
    noir = 8
    crime = 9
    detective = 10
    cartoon = 11
    comedy = 12
    family = 13
    western = 14
    history = 15
    biography = 16
    sport = 17
    adventures = 18
    melodrama = 19
    drama = 20
    child = 21
    musical = 22

class User:
    def __init__(self,id,):
        self.user_id = id
        self.user_type = "usu"
        user_list.append(self)
class Person:
    def __init__(self, person_id, full_name, positions, start_year, end_year):
        self.person_id = person_id
        self.full_name = full_name
        self.positions = positions
        self.start_year = start_year
        self.end_year = end_year

bot = telebot.TeleBot(os.environ["TOKEN"])
bot_chat = {}
user_list = []
person_list = [
    Person(0,"Уилл Смит",0,1985,2021),
    Person(1,"Вин Дизель",1,1980,2021),
    Person(2,"Скарлетт Йохансон",2,1920,2021),
    Person(3,"Уилл Смит",3,1920,1977)
]

def user_adder(id):
    user = User(id)
    bot_chat[user.user_id] = {
        "id": None,
        "help": None,
        "markup": None,
        "first_message": None,
        "select": {
            "id": None,
            "name": None,
            "stage": None,
            "target": None,
            "genre": [],
            "date_start": None,
            "date_end": None,
            "person": []
        }
    }
def user_finder(id):
    for i in range(len(user_list)):
        user = user_list[i]
        if user.user_id == id:
            return user
def user_checker(id):
    if user_finder(id) != None:
        return True
    else:
        return False

def person_mas_pointer(mas):
    stroke = ""
    for i in range(len(mas)):
        stroke += stroke_personer(mas[i])
    return stroke
def person_name_filter(name):
    result = []
    for i in range(len(person_list)):
        if person_list[i].full_name == name:
            result.append(person_list[i])
    return result

def stroke_pointer(stroke):
    return f"* {stroke}\n"
def stroke_personer(person):
    return f"*/p_id_{'0' * (4 - len(str(person.person_id)))}{person.person_id}; Полное имя: {person.full_name}; Период: {person.start_year}-{person.end_year}\n"
def stroke_sectioner(stroke):
    return f"{stroke}\n-----\n"
def stroke_mas_pointer(mas):
    stroke = ""
    for i in range(len(mas)):
        stroke += f"* {mas[i].full_name} \n"
    return stroke

def select_idifer(message,targetVal):
    return None
def select_targer(message,targetVal):
    bot_chat[message.chat.id]["select"]["target"] = targetVal
def select_stager(message,stageVal):
    bot_chat[message.chat.id]["select"]["stage"] = stageVal

def message_send(chatId,stroke,markup):
    if markup != None:
        bot.send_message(chatId,stroke,reply_markup=markup)
    else:
        bot.send_message(chatId,stroke)
def message_help_sender(chatId):
    stroke = stroke_sectioner("Здесь вы сможете ознакомиться со списком команд для данного бота:")
    stroke += stroke_pointer("/id - Отобразит ваш идентификатор в Телеграмме.")
    stroke += stroke_pointer("/func - Отобразит перечень функций данного приложения.")
    stroke += stroke_pointer("/help - Отобразит текущий список команд для данного бота.")
    return bot.send_message(chatId,stroke)

def functional_geter():
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton("Получить список кино-персон",callback_data="persons"))
    keyboard.row(telebot.types.InlineKeyboardButton("Построить граф связей кино-персоны",callback_data="graf"))
    keyboard.row(telebot.types.InlineKeyboardButton("Получить список фильмов кино-персоны",callback_data="person_films"))
    keyboard.row(telebot.types.InlineKeyboardButton("Получить хронологию связей кино-персоны",callback_data="cron"))
    return keyboard

def functional_graf_geter(call):
    select_targer(call.message,Target.graf.value)
    select_stager(call.message,Stage.nameSelect.value)
    bot.edit_message_text("* Получить граф кино-персоны",call.message.chat.id,bot_chat[call.message.chat.id]["markup"].id)
    message = bot.send_message(call.message.chat.id,"Укажите полное имя искомого актёра: ")
async def functional_graf_pid_selecter(message):
    bot.send_message(message.chat.id,"Вы выбрали персону!")
    return None
async def functional_graf_name_selecter(message):
    person = person_name_filter(message.text)
    if len(person) == 1:
        bot_chat[message.chat.id]["select"]["person"] = person[0]
        bot_chat[message.chat.id]["select"]["stage"] = Stage.generSelect.value
        bot.send_message(message.chat.id,stroke_personer(person[0]))
    elif len(person) > 1:
        bot_chat[message.chat.id]["select"]["person"] = person
        bot_chat[message.chat.id]["select"]["stage"] = Stage.idSelect.value
        bot.send_message(message.chat.id,stroke_sectioner("Найденные соответствия:") + person_mas_pointer(person))
        await asyncio.sleep(1)
        bot.send_message(message.chat.id,"Выберите `p_id` из перечня, чтобы однозначно определить нужного актёра.")
    else:
        bot.send_message(message.chat.id,len(person)) # У
        bot.send_message(message.chat.id,"Соответствия не найдены")

def functional_cron_geter(call):
    bot_chat[call.message.chat.id]["select"]["target"] = Target.cron.value
    bot.send_message(call.message.chat.id,"`Хронология`")

def functional_persons_geter(call):
    bot_chat[call.message.chat.id]["select"]["target"] = Target.persons.value
    bot.edit_message_text("* Получить список кино-персон",call.message.chat.id,bot_chat[call.message.chat.id]["markup"].id)
    stroke = ""
    for i in range(len(person_list)):
        string = f"ID: {'0' * (4-len(str(person_list[i].person_id)))}{person_list[i].person_id}; "
        string += f"{person_list[i].full_name}; "
        string += f"Период: {str(person_list[i].start_year)}-{str(person_list[i].end_year)}; "
        stroke += stroke_pointer(string)
    bot.send_message(call.message.chat.id,stroke)

def functional_person_films_geter(call):
    bot_chat[call.message.chat.id]["select"]["target"] = Target.person_films.value
    print(Target.person_films.value)
    bot.send_message(call.message.chat.id,"`Список фильмов с участием персоны`")

async def dialog_first_messanger(chatId,user):
    bot_chat[user.user_id]["first_message"] = bot.send_message(chatId,"Приветствуем вас, уважаемый пользователь!")
    await asyncio.sleep(1)
    bot_chat[user.user_id]["help"] = message_help_sender(chatId)
    await asyncio.sleep(1)
    bot_chat[user.user_id]["markup"] = bot.send_message(chatId,"Какой функционал вы желаете использовать?",reply_to_message_id=True,reply_markup=functional_geter())
def dialog_target_messanger(chatId,user):
    return None

@bot.message_handler(commands=["id","func","help","p_id"])
def help_commander(message):
    if user_finder(message.chat.id):
        if bot_chat[message.chat.id]["first_message"] != None:
            bot.delete_message(message.chat.id,bot_chat[message.chat.id]["first_message"].id)
            bot_chat[message.chat.id]["first_message"] = None
        
        if message.text == "/id":
            if bot_chat[message.chat.id]["id"] != None:
                bot.delete_message(message.chat.id,bot_chat[message.chat.id]["id"].id)
            bot_chat[message.chat.id]["id"] = bot.send_message(message.chat.id,f"Ваш ID: {message.chat.id}")
        elif message.text == "/func":
            if bot_chat[message.chat.id]["markup"] != None:
                bot.delete_message(message.chat.id,bot_chat[message.chat.id]["markup"].id)
            bot_chat[message.chat.id]["markup"] = bot.send_message(message.chat.id,"Какой функционал вы желаете использовать?",reply_markup=functional_geter())
        elif message.text == "/help":
            if bot_chat[message.chat.id]["help"] != None:
                bot.delete_message(message.chat.id,bot_chat[message.chat.id]["help"].id)
            bot_chat[message.chat.id]["help"] = message_help_sender(message.chat.id)
        
        if bot_chat[message.chat.id]["select"]["target"] != None:
            print(message.text.find("/p_id"))
            if message.text.find("/p_id") != -1:
                bot_chat[message.chat.id]["select"]["id"] == int(message.text.split(" ")[2])
                bot.send_message(message.chat.id,bot_chat[message.chat.id]["select"]["id"])
@bot.message_handler(content_types=["text"])
def text_determinant(message):
    if user_finder(message.from_user.id):
        chat_select = bot_chat[message.chat.id]["select"]
        if chat_select["stage"] == Stage.nameSelect.value:
            asyncio.run(functional_graf_name_selecter(message))
        elif chat_select["stage"] == Stage.idSelect.value:
            asyncio.run(functional_graf_pid_selecter(message))
    else:
        user_adder(message.from_user.id)
        asyncio.run(dialog_first_messanger(message.chat.id,user_finder(message.from_user.id)))

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == "cron":
        functional_cron_geter(call)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    elif call.data == "graf":
        functional_graf_geter(call)
        #bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    elif call.data == "persons":
        functional_persons_geter(call)
    elif call.data == "person_films":
        functional_person_films_geter(call)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
bot.polling()