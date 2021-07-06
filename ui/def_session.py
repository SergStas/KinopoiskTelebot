from class_ui import *

def session_adder(bot_session,chat_id,bot):
    session = Session(id,bot)
    bot_session.append(session)
    return session
def session_finder(bot_session,chat_id):
    for i in bot_session:
        if i.id == chat_id:
            return i
    return None