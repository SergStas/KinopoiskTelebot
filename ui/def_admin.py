import asyncio
from class_ui import *
from def_dialog import *

def admin_adder(bot,bot_session,id,user_name):
    session = Session(id,bot,user_name)
    session.user.type = "adm"
    bot_session.append(session)
    asyncio.run(admin_introduction_geter(session))
def admin_finder(bot_session,id):
    for i in bot_session:
        if i.user.id == id:
            return i
def admin_mas_adder(bot,bot_adm_session,ids):
    for id in ids:
        session = Session(id)
        session.user.type = "adm"
        bot_adm_session.append(session)
