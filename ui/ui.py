# TODO: Nikita 1170650256

import os
import re
import telebot
import asyncio
import datetime
from datetime import *
from class_ui import *
from def_user import *
from def_admin import *
from def_stroke import *
from def_select import *
from def_dialog import *
from def_session import *
from def_section import *
from typing import AsyncContextManager
from telebot.apihelper import delete_message
from asyncio.subprocess import create_subprocess_shell

# bot = telebot.TeleBot(os.environ["TOKEN"])
bot = telebot.TeleBot("1840456562:AAEVs2Teifyfojb3ep_FctSburLggTHy_00")
bot_session = []
bot_adm_session = []
bot_bos_session = []
bot_usu_session = []

bot_chat = {}
boss_id_list = [
    632012083
],
admin_id_list = [
    361877365,
    426134463,
    1839000131,
    1170650256
]
person_list = [
    Person(0,"act","Уилл Смит",0,1985,2021,open("./Уилл_Смит.png","rb")),
    Person(1,"act","Вин Дизель",1,1980,2021,open("./Вин_Дизель.png","rb")),
    Person(2,"act","Скарлетт Йохансон",2,1920,2021,open("./Скарлетт_Йохансон.png","rb")),
    Person(3,"act","Уилл Смит",3,1920,1977,open("./Левый_Чел.png","rb"))
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
user_mas_adder(bot,bot_usu_session,testers_usu)


@bot.callback_query_handler(func=lambda call: True)
def call_determenant(call):
    bot_session.extend(bot_bos_session)
    bot_session.extend(bot_adm_session)
    bot_session.extend(bot_usu_session)
    session = session_finder(bot_session,call.message.chat.id)
    if call.data == "up_usu_list":
        markup_usu_list_rechanger(bot_usu_session,session,True)
    elif call.data == "down_usu_list":
        markup_usu_list_rechanger(bot_usu_session,session,False)
    elif call.data == "up_adm_list":
        markup_adm_list_rechanger(bot_adm_session,session,True)
    elif call.data == "up_adm_list":
        markup_adm_list_rechanger(bot_usu_session,session,False)
    elif call.data == "cron":
        asyncio.run(cron_selecter(session))
    elif call.data == "graf":
        asyncio.run(graf_selecter(session))
    elif call.data.find("get_usu") != -1:
        user_info_geter(session,bot_usu_session[int(call.data.split("_")[2])])
    if session.select.stage == Stage.typeSelect.value:
        if call.data == "set_act" or call.data == "set_stf":
            asyncio.run(functional_type_selecter(session,call.data.split("_")[1]))
    if session.select.stage == Stage.idSelect.value:
        if call.data.find("set_pers") != -1:
            asyncio.run(functional_pid_selecter(session,int(call.data.split("_")[2])))
            return None
    if session.select.stage == Stage.generSelect.value:
        print(call.data)
        if call.data.find("gener_add") != -1 or call.data.find("gener_remove") != -1:
            asyncio.run(functional_gener_selecter(session,call.data))
            return None
        if call.data == "done":
            asyncio.run(functional_gener_selecter(session,call.data))
            return None
        if call.data == "none":
            return None
    if session.select.stage == Stage.rankSelect.value:
        if call.data.find("set") != -1:
            asyncio.run(functional_rank_selecter(session,int(call.data.split("_")[1])))
    if session.select.stage == Stage.result.value:
        if call.data == "done" or call.data == "cancel":
            asyncio.run(functional_result_selecter(session,call.data))
    bot_session.clear()
@bot.message_handler(commands=[
    "id",
    "func",
    "help",
    "clear",
    "get_users",
    "get_admins"])
def command_determinant(message):
    bot_session.extend(bot_bos_session)
    bot_session.extend(bot_adm_session)
    bot_session.extend(bot_usu_session)
    session = session_finder(bot_session,message.chat.id)
    if session != None:
        if session.user.date_last != date.today():
            session.user.date_last = date.today()
        if message.text == "/id":
            id_geter(session)
        elif message.text == "/func":
            func_geter(session)
        elif message.text == "/help":
            help_geter(session)
        elif message.text == "/clear":
            clear_geter(session)
        elif message.text == "/get_users":
            asyncio.run(users_geter(bot_usu_session,session))
        elif message.text == "/get_admins":
            asyncio.run(admins_geter(bot_adm_session,session))
@bot.message_handler(content_types=["text"])
def message_determinant(message):
    bot_session.extend(bot_bos_session)
    bot_session.extend(bot_adm_session)
    bot_session.extend(bot_usu_session)
    session = session_finder(bot_session,message.chat.id)
    if session != None:
        if session.user.date_last != date.today():
            session.user.date_last = date.today()
        if session.select.stage == Stage.nameSelect.value:
            asyncio.run(functional_name_selecter(session,message,person_list))
        elif session.select.stage == Stage.thresholdSelect.value:
            asyncio.run(functional_treshold_selecter(session,message.text))
    else:
        for i in admin_id_list:
            if i == message.chat.id:
                print(f"* new_user. name: {message.from_user.username};")
                admin_adder(bot,bot_adm_session,message.chat.id,message.from_user.username)
                bot_session.clear()
                return None
        print(f"* new_user. name: {message.from_user.username};")
        user_adder(bot,bot_usu_session,message.chat.id,message.from_user.username)
        bot_session.clear()
        return None
   #asyncio.run(functional_start_year_selecter(bot,message))
bot.polling(none_stop=True)