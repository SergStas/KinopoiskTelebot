# TODO: Nikita

import os
import telebot
import asyncio
from PIL import Image,ImageFilter
from telebot.apihelper import delete_message

class User:
    def __init__(self,id,):
        self.id = id
        self.type = "usu"
        user_list.append(self)

bot = telebot.TeleBot(os.environ["TOKEN"])
bot_chat = {}
user_list = []
person_list = []

def user_adder(id):
    user = User(id)
    bot_chat[user.id] = {
        "id": None,
        "help": None,
        "markup": None,
        "first_message": None,
    }
def user_finder(id):
    for i in range(len(user_list)):
        user = user_list[i]
        if user.id == id:
            return user
def user_checker(id):
    if user_finder(id) != None:
        return True
    else:
        return False

def stroke_pointer(stroke):
    return f"* {stroke}\n"
def stroke_sectioner(stroke):
    return f"{stroke}\n-----\n"

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
    stroke += stroke_pointer("/restart - Перезапустит бота.")
    stroke += stroke_pointer("/profile_drop - Удалит ваши данные, хранящиеся в приложении.")
    return bot.send_message(chatId,stroke)

def functional_geter():
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton("Получить список кино-персон",callback_data="persons"))
    keyboard.row(telebot.types.InlineKeyboardButton("Построить граф связей кино-персоны",callback_data="graf"))
    keyboard.row(telebot.types.InlineKeyboardButton("Получить список фильмов кино-персоны",callback_data="person_films"))
    keyboard.row(telebot.types.InlineKeyboardButton("Получить хронологию связей кино-персоны",callback_data="cron"))
    return keyboard
def functional_graf_geter(call):
    bot.send_message(call.message.chat.id,"`Граф`")
def functional_cron_geter(call):
    bot.send_message(call.message.chat.id,"`Хронология`")
def functional_persons_geter(call):
    bot.send_message(call.message.chat.id,"`Список персон`")
def functional_person_films_geter(call):
    bot.send_message(call.message.chat.id,"`Список фильмов с участием персоны`")

async def dialog_first_messanger(chatId,user):
    bot_chat[user.id]["first_message"] = bot.send_message(chatId,"Приветствуем вас, уважаемый пользователь!")
    await asyncio.sleep(1)
    bot_chat[user.id]["help"] = message_help_sender(chatId)
    await asyncio.sleep(1)
    bot_chat[user.id]["markup"] = bot.send_message(chatId,"Какой функционал вы желаете использовать?",reply_to_message_id=True,reply_markup=functional_geter())
def dialog_target_messanger(chatId,user):
    return None

@bot.message_handler(commands=["id","func","help"])
def help_commander(message):
    if user_finder(message.from_user.id):
        if bot_chat[message.from_user.id]["first_message"] != None:
            bot.delete_message(message.chat.id,bot_chat[message.from_user.id]["first_message"].id)
            bot_chat[message.from_user.id]["first_message"] = None
        if message.text == "/id":
            if bot_chat[message.from_user.id]["id"] != None:
                bot.delete_message(message.chat.id,bot_chat[message.from_user.id]["id"].id)
            bot_chat[message.from_user.id]["id"] = bot.send_message(message.chat.id,f"Ваш ID: {message.from_user.id}")
        elif message.text == "/func":
            if bot_chat[message.from_user.id]["markup"] != None:
                bot.delete_message(message.chat.id,bot_chat[message.from_user.id]["markup"].id)
            bot_chat[message.from_user.id]["markup"] = bot.send_message(message.chat.id,"Какой функционал вы желаете использовать?",reply_markup=functional_geter())
        elif message.text == "/help":
            if bot_chat[message.from_user.id]["help"] != None:
                bot.delete_message(message.chat.id,bot_chat[message.from_user.id]["help"].id)
            bot_chat[message.from_user.id]["help"] = message_help_sender(message.chat.id)

@bot.message_handler(content_types=["text"])
def text_determinant(message):
    if user_finder(message.from_user.id):
        dialog_target_messanger(message.chat.id,user_finder(message.chat.id))
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
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    elif call.data == "persons":
        functional_persons_geter(call)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    elif call.data == "person_films":
        functional_person_films_geter(call)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
bot.polling()