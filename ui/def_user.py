import asyncio
from class_ui import *
from def_dialog import *

def user_adder(bot,bot_session,id,user_name):
    session = Session(id,bot,user_name)
    bot_session.append(session)
    asyncio.run(user_introdaction_geter(session))
def user_finder(mas,id):
    for i in mas:
        if mas[i].user_id == id:
            return mas[i]
    return None
def user_checker(mas,id):
    for i in mas:
        if mas[i].user_id == id:
            return True
    else:
        return False
def user_mas_adder(bot,bot_usu_session,ids):
    name = "usu"
    count = 0
    for id in ids:
        session = Session(id,bot,f"{name}_{count}")
        bot_usu_session.append(session)
        count += 1