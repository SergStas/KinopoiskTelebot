import asyncio
import telebot
from class_ui import *
from def_stroke import *
from def_select import *
from def_section import *
from telebot.apihelper import delete_message

def replacer(mas,val1,val2):
    mas = mas.insert(val1,val2)
    return mas  

def markup_clearer(session):
    if session.message_markup.markup != None:
        session.bot.delete_message(session.id,session.message_markup.id)
        session.message_markup = Markup()
    if len(session.message_markup.markup_selector) > 0:
        for i in session.message_markup.markup_selector:
            session.bot.delete_message(session.id,i)
        session.message_markup.markup_selector.clear()
def markup_selector_clearer(session):
    if len(session.message_markup.markup_selector) > 0:
        for i in session.message_markup.markup_selector:
            session.bot.delete_message(session.id,i)
        session.message_markup.markup_selector.clear()
def stage_messages_id_clearer(session):
    for i in session.stage_messages_id:
        session.bot.delete_message(session.id,i)
    session.stage_messages_id.clear()

def markup_per_changer(session,person):
    return None
def markup_adm_list_rechanger(bot_session,session,val):
    limit = 10
    endIndex = 0
    startIndex = 0
    bot_session_len = len(bot_session)
    if bot_session_len == 0:
        return None
    if val == True:
        if session.message_markup.index == 0:
            return None
        startIndex = session.message_markup.index - limit
        endIndex = startIndex + limit
        session.message_markup.index -= limit
    elif val == False:
        if session.message_markup.index + limit > bot_session_len:
            return None
        startIndex += session.message_markup.index + limit
        endIndex = startIndex + limit
        session.message_markup.index += limit
    session.message_markup.markup = telebot.types.InlineKeyboardMarkup()
    for i in range(startIndex,endIndex):
        if i > bot_session_len - 1:
            session.message_markup.markup.row(telebot.types.InlineKeyboardButton("-",callback_data="get-"))
        else:
            session.message_markup.markup.row(telebot.types.InlineKeyboardButton(f"ID: {'0' * (4 - len(str(i)))}{i} - {bot_session[i].user.name}",callback_data="get-"))
    session.message_markup.markup.row(
        telebot.types.InlineKeyboardButton("▲",callback_data="up_adm_list"),
        telebot.types.InlineKeyboardButton("▼",callback_data="down_adm_list")
    )
    session.bot.edit_message_text(chat_id=session.id,message_id=session.message_markup.id,text="Список администраторов:",reply_markup=session.message_markup.markup)
def markup_usu_list_rechanger(bot_session,session,val):
    limit = 10
    endIndex = 0
    startIndex = 0
    bot_session_len = len(bot_session)
    if bot_session_len == 0:
        return None
    if val == True:
        if session.message_markup.index == 0:
            return None
        startIndex = session.message_markup.index - limit
        endIndex = startIndex + limit
        session.message_markup.index -= limit
    elif val == False:
        if session.message_markup.index + limit > bot_session_len:
            return None
        startIndex += session.message_markup.index + limit
        endIndex = startIndex + limit
        session.message_markup.index += limit
    session.message_markup.markup = telebot.types.InlineKeyboardMarkup()
    for i in range(startIndex,endIndex):
        if i > bot_session_len - 1:
            session.message_markup.markup.row(telebot.types.InlineKeyboardButton("-",callback_data="none"))
        else:
            session.message_markup.markup.row(telebot.types.InlineKeyboardButton(f"ID: {'0' * (4 - len(str(i)))}{i} - {bot_session[i].user.name}",callback_data=f"get_usu_{i}"))
    session.message_markup.markup.row(
        telebot.types.InlineKeyboardButton("▲",callback_data="up_usu_list"),
        telebot.types.InlineKeyboardButton("▼",callback_data="down_usu_list")
    )
    session.bot.edit_message_text(chat_id=session.id,message_id=session.message_markup.id,text="Список пользователей:",reply_markup=session.message_markup.markup)
def markup_date_rechanger(session,val):
    if val == "left" and session.message_markup.first_date != 1920:
        session.message_markup.first_date -= 30
        session.message_markup.markup = markup_date_geter(session.message_markup.first_date)
        session.bot.edit_message_text(chat_id=session.id,message_id=session.message_markup.id,text="* Выберите начальную дату: ",reply_markup=session.message_markup.markup)
    elif val == "right":
        session.message_markup.first_date += 30
        session.message_markup.markup = markup_date_geter(session.message_markup.first_date)
        session.bot.edit_message_text(chat_id=session.id,message_id=session.message_markup.id,text="* Выберите начальную дату: ",reply_markup=session.message_markup.markup)