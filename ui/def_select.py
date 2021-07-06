import asyncio
import telebot
import datetime
from class_ui import *
from telebot.apihelper import delete_message

def markup_date_geter(year_first):
    markup = telebot.types.InlineKeyboardMarkup()
    for count1 in range(5):
        row = []
        count = 0
        for count2 in range(year_first,year_first + 6):
            row.append(telebot.types.InlineKeyboardButton(f"{count2}",callback_data=f"set_{count2}"))
            count += 1
        markup.row(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            row[5]
        )
        year_first += 6
    markup.row(
        telebot.types.InlineKeyboardButton("<=",callback_data="left"),
        telebot.types.InlineKeyboardButton("=>",callback_data="right"),
    )
    return markup
