import re
import asyncio
import telebot
from class_ui import *
from def_stroke import *
from def_select import *
from def_section import *
from telebot.apihelper import delete_message

def id_geter(session):
    if session.message_id != None:
        session.bot.delete_message(session.id,session.message_id)
    session.message_id = session.bot.send_message(session.id,stroke_pointer(f"Ваш ID: {session.id}")).id
def func_geter(session):
    markup_clearer(session)
    session.message_markup.markup = telebot.types.InlineKeyboardMarkup()
    session.message_markup.markup.row(telebot.types.InlineKeyboardButton("Получить список кино-персон",callback_data="persons"))
    session.message_markup.markup.row(telebot.types.InlineKeyboardButton("Построить граф связей кино-персоны",callback_data="graf"))
    session.message_markup.markup.row(telebot.types.InlineKeyboardButton("Получить список фильмов кино-персоны",callback_data="person_films"))
    session.message_markup.markup.row(telebot.types.InlineKeyboardButton("Построить хронологию связей кино-персоны",callback_data="cron"))
    session.message_markup.markup = session.bot.send_message(session.id,"Какой функционал бота вы желаете задействовать?",reply_markup=session.message_markup.markup)
    session.message_markup.id = session.message_markup.markup.id
def help_geter(session):
    if session.message_help != None:
        session.bot.delete_message(session.id,session.message_help)
    if session.user.type == "usu":
        session.message_help = session.bot.send_message(
            session.id,
            stroke_sectioner("Здесь вы можете ознакомиться со списком команд, для взаимодействия с ботом:") +         
            stroke_pointer("/id - Получить Ваш ID в Телеграмме.") +
            stroke_pointer("/help - Получить список стандартных команд данного бота.") +
            stroke_pointer("/func - Получить перечень функций данного бота.") +
            stroke_pointer("/clear - Очистить все сообщения данного бота.") +
            stroke_pointer("/store - Получить Вашу историю запросов.") +
            stroke_pointer("/choosen - Получить список Ваших избранных запросов.")
        ).id
    elif session.user.type == "adm":
        session.message_help = session.bot.send_message(
        session.id,
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
    ).id
    elif session.user.type == "bos":
        return None
def clear_geter(session):
    if session.message_id != None:
        session.bot.delete_message(session.id,session.message_id)
        session.message_id = None
    if session.message_info != None:
        session.bot.delete_message(session.id,session.message_info)
        session.message_info = None
    if session.message_help != None:
        session.bot.delete_message(session.id,session.message_help)
        session.message_help = None
    if session.select.target != None:
        session.select = Select()
        if session.select.message_select != None:
            session.bot.delete_message(session.id,session.select.message_select)
    if session.message_markup.markup != None:
        session.bot.delete_message(session.id,session.message_markup.id)
        session.message_markup = Markup()
    if len(session.stage_messages_id) > 0:
        for i in session.stage_messages_id:
            session.bot.delete_message(session.id,i)
        session.stage_messages_id.clear()
    if len(session.message_markup.markup_selector) > 0:
        for i in session.message_markup.markup_selector:
            session.bot.delete_message(session.id,i)
        session.message_markup.markup_selector.clear()
    for i in range(len(session.messages_id)):
        session.bot.delete_message(session.id,session.messages_id[i])
    session.messages_id.clear()
    session.messages_id.append(session.bot.send_message(session.id,"Вы можете просмотреть команды бота с помощью команды /help").id)
def user_info_geter(session,usu_session):
    if session.message_info != None:
        session.bot.delete_message(session.id,session.message_info)
        session.message_info = None
    if usu_session != None:
        stroke = stroke_sectioner(f"Информация по пользователю `{usu_session.user.name}`:")
        stroke += stroke_pointer(f"Имя: {usu_session.user.name};")
        stroke += stroke_pointer(f"Тип: {usu_session.user.type};")
        stroke += stroke_pointer(f"Дата регистрации: {usu_session.user.date_start};")
        stroke += stroke_pointer(f"Дата посещения: {usu_session.user.date_last};")
        session.message_info = session.bot.send_message(session.id,stroke).id
    else:
        session.message_info = session.bot.send_message(session.id,"Данный пользователь не существует.").id
async def pers_geter(session,message):
    if message.text == "stf":
        return None
    elif message.text == "act":
        return None
async def users_geter(bot_session,session):
    if session.message_markup != None:
        markup_clearer(session)
    if session.user.type != "usu":
        session.message_markup.index = 0
        session.message_markup.markup = telebot.types.InlineKeyboardMarkup()
        session.messages_id.append(session.bot.send_message(session.id,"Вы можете получить более подробную информацию по конкретному пользователю, выбрав его в списке.").id)
        for i in range(10):
            if i == 10: break
            if bot_session[i].user.type != "usu": continue
            if i <= len(bot_session) - 1:
                session.message_markup.markup.row(telebot.types.InlineKeyboardButton(f"№{'0' * (4 - len(str(i)))}{i} - {bot_session[i].user.name}",callback_data=f"get_usu_{i}"))
            else:
                session.message_markup.markup.row(telebot.types.InlineKeyboardButton("-",callback_data="none"))
        session.message_markup.markup.row(
            telebot.types.InlineKeyboardButton("▲",callback_data="up_usu_list"),
            telebot.types.InlineKeyboardButton("▼",callback_data="down_usu_list")
        )
        await asyncio.sleep(1)
        session.message_markup.markup = session.bot.send_message(session.id,"Список пользователей:",reply_markup=session.message_markup.markup)
        session.message_markup.id = session.message_markup.markup.id
async def admins_geter(bot_adm_session,session):
    if session.user.type != "usu" and session.user.type != "adm":
        if session.message_markup != None:
            markup_clearer(session)
        session.message_markup = Markup()
        session.message_markup.index = 0
        session.message_markup.markup = telebot.types.InlineKeyboardMarkup()
        session.messages_id.append(session.bot.send_message(session.id,"Вы можете получить более подробную информацию по конкретному пользователю, выбрав его в списке.").id)
        for i in range(10):
            if i == 10: break
            if i < len(bot_adm_session):
                session.message_markup.markup.row(telebot.types.InlineKeyboardButton(f"№{'0' * (4 - len(str(i)))}{i} - {bot_adm_session[i].user.name}",callback_data="get-"))
            elif i > len(bot_adm_session):
                session.message_markup.markup.row(telebot.types.InlineKeyboardButton("-",callback_data="get-"))
        session.message_markup.markup.row(
            telebot.types.InlineKeyboardButton("▲",callback_data="up_adm_list"),
            telebot.types.InlineKeyboardButton("▼",callback_data="down_adm_list")
        )
        await asyncio.sleep(1)
        session.message_markup.markup = session.bot.send_message(session.id,"Список администраторов:",reply_markup=session.message_markup.markup)
        session.message_markup.id = session.message_markup.markup.id

async def user_introdaction_geter(session):
    session.messages_id.append(session.bot.send_message(session.id,"Добро пожаловать, уважаемый пользователь!").id)
    await asyncio.sleep(1)
    help_geter(session)
    await asyncio.sleep(1)
    func_geter(session)
async def admin_introduction_geter(session):
    session.messages_id.append(session.bot.send_message(session.id,"Добро пожаловать, уважаемый администратор!").id)
    await asyncio.sleep(1)
    help_geter(session)
    await asyncio.sleep(1)
    func_geter(session)

async def graf_selecter(session):
    session.select = Select()
    session.select.stage = Stage.typeSelect.value
    session.select.stage_complete = [False,False,False,False]
    session.select.target = Target.graf.value
    markup_clearer(session)
    session.messages_id.append(session.bot.send_message(session.id,stroke_pointer("Выбрано: Построение графа связей кино-персоны.")).id)
    await asyncio.sleep(1)
    session.message_markup.markup = telebot.types.InlineKeyboardMarkup()
    session.message_markup.markup.row(
        telebot.types.InlineKeyboardButton("Поиск персонала",callback_data="set_stf"),
        telebot.types.InlineKeyboardButton("Поиск актёра",callback_data="set_act")
    )
    session.message_markup.id = session.bot.send_message(session.id,stroke_pointer("1/4. Укажите тип кино-персоны, которую необходимо найти:"),reply_markup=session.message_markup.markup).id
async def cron_selecter(session):
    session.select = Select()
    session.select.stage = Stage.startYearSelect.value
    session.select.target = Target.cron.value
    markup_clearer(session)
    session.messages_id.append(session.bot.send_message(session.id,stroke_pointer("Выбрано: Построение хронологии;")).id)
    await asyncio.sleep(1)
    session.message_markup.markup = markup_date_geter(1920)
    session.message_markup.id = session.bot.send_message(session.id,"_" * 19 + " Выберите_начальную_дату " + "_" * 18,reply_markup=session.message_markup.markup).id
    session.message_markup.markup.date_first = 1920

async def functional_pid_selecter(session,num):
    session.select.person = session.select.person[num]
    session.select.stage = Stage.generSelect.value
    markup_selector_clearer(session)
    stage_messages_id_clearer(session)
    session.messages_id.append(session.bot.send_message(session.id,stroke_pointer(f"Была выбрана персона: {session.select.person.full_name}")).id)
    await asyncio.sleep(1)
    session.message_markup.markup = telebot.types.InlineKeyboardMarkup()
    for i in Gener:
        session.message_markup.markup.row(
            telebot.types.InlineKeyboardButton(f"{i.name}",callback_data=f"gener_add_{i.value}"),
            telebot.types.InlineKeyboardButton("-",callback_data=f"gener_remove_{i.value}")
        )
    session.message_markup.markup.row(
        telebot.types.InlineKeyboardButton("Готово",callback_data="done")
    )
    session.message_markup.id = session.bot.send_message(session.id,stroke_sectioner("Список жанров:"),reply_markup=session.message_markup.markup).id
    await asyncio.sleep(1)
    session.stage_messages_id.append(session.bot.send_message(session.id,"Выбирите из списка те жанры, по которым необходимо осуществить поиск, нажав на соответсвующую кнопку. При желании, жанр можно откатить, выбрав его по тому же принципу.").id)
async def functional_rank_selecter(session,num):
    markup_clearer(session)
    stage_messages_id_clearer(session)
    session.select.stage = Stage.thresholdSelect.value
    session.select.rank = num
    session.messages_id.append(session.bot.send_message(session.id,stroke_pointer(f"Было выбрано значение `коленьев`: {num};")).id)
    await asyncio.sleep(1)
    session.stage_messages_id.append(session.bot.send_message(session.id,"Укажите количество общих фильмов данной персоны с другими кино-персонами:").id)
async def functional_type_selecter(session,type):
    session.select.stage = Stage.nameSelect.value
    session.select.type = type
    markup_clearer(session)
    if type == "act":
        session.messages_id.append(session.bot.send_message(session.id,stroke_pointer("Выбрано: Поиск по актёрам;")).id)
    elif type == "stf":
        session.messages_id.append(session.bot.send_message(session.id,stroke_pointer("Выбрано: Поиск по персоналу;")).id)
    await asyncio.sleep(1)
    session.stage_messages_id.append(session.bot.send_message(session.id,"2/4. Введите полное имя искомой персоны:").id)
async def functional_name_selecter(session,message,persons):
    result = []
    for i in persons:
        if i.full_name == message.text:
            result.append(i)
    len_result = len(result)
    if len_result > 1:
        session.select.stage = Stage.idSelect.value
        session.select.person = []
        session.stage_messages_id.append(session.bot.send_message(session.id,"Найдено множество соответствий!").id)
        await asyncio.sleep(1)
        session.stage_messages_id.append(session.bot.send_message(session.id,"Укажите правильное совпадение:").id)
        await asyncio.sleep(1)
        for i in range(len(result)):
            session.select.person.append(result[i])
            markup = telebot.types.InlineKeyboardMarkup()
            markup.row(telebot.types.InlineKeyboardButton("Выбрать",callback_data=f"set_pers_{i}"))
            session.message_markup.markup_selector.append(session.bot.send_photo(session.id,result[i].photo).id)
            session.message_markup.markup_selector.append(session.bot.send_message(session.id,f"Годы деятельности: {result[i].start_year}-{result[i].end_year}; Имя: {result[i].full_name};",reply_markup=markup).id)
    elif len_result == 1:
        session.select.person = result[0]
        session.select.stage = Stage.generSelect.value
        session.messages_id.append(session.bot.send_message(session.id,"Найдено однозначеное соответствие!").id)
        if result[0].photo != None:
            await asyncio.sleep(1)
            session.messages_id.append(session.bot.send_photo(session.id,result[0].photo).id)
        await asyncio.sleep(1)
        session.messages_id.append(session.bot.send_message(session.id,f"Годы деятельности: {result[0].start_year}-{result[0].end_year}; Имя: {result[0].full_name};").id)
        await asyncio.sleep(1)
        session.message_markup.markup = telebot.types.InlineKeyboardMarkup()
        for i in Gener:
            session.message_markup.markup.row(
                telebot.types.InlineKeyboardButton(f"{i.name}",callback_data=f"gener_add_{i.value}"),
                telebot.types.InlineKeyboardButton("-",callback_data=f"gener_remove_{i.value}")
            )
        session.message_markup.markup.row(
            telebot.types.InlineKeyboardButton("Готово",callback_data="done")
        )
        session.message_markup.id = session.bot.send_message(session.id,stroke_sectioner("Список жанров:"),reply_markup=session.message_markup.markup).id
        await asyncio.sleep(1)
        session.stage_messages_id.append(session.bot.send_message(session.id,"Выбирите из списка те жанры, по которым необходимо осуществить поиск, нажав на соответсвующую кнопку. При желании, жанр можно откатить, выбрав его по тому же принципу.").id)
    elif len_result == 0:
        session.messages_id.append(session.bot.send_message(session.id,"Соостветсвие не найдено!").id)
        await asyncio.sleep(1)
        session.messages_id.append(session.bot.send_message(session.id,"Попробуйте повторить попытку.").id)
async def functional_step_selecter(session,command):
    session.message_markup.markup = telebot.types.InlineKeyboardMarkup()
    session.message_markup.markup.row(
        telebot.types.InlineKeyboardButton("-10",callback_data="inc_10"),
        telebot.types.InlineKeyboardButton("-5",callback_data="inc_5"),
        telebot.types.InlineKeyboardButton("-1",callback_data="inc_1"),
        telebot.types.InlineKeyboardButton("+1",callback_data="add_1"),
        telebot.types.InlineKeyboardButton("+5",callback_data="add_5"),
        telebot.types.InlineKeyboardButton("+10",callback_data="add_10")
    )
    session.message_markup.markup.row(telebot.types.InlineKeyboardButton("Принять",callback_data="done"))
    session.message_markup.id = session.bot.send_message(session.id,stroke_sectioner("Укажите значение интервалов, на которые будет необходимо разделить указанный период:") + stroke_pointer("Текущее значение: 0"),reply_markup=session.message_markup.markup).id
async def functional_gener_selecter(session,command):
    session.message_markup.markup = telebot.types.InlineKeyboardMarkup()
    if command == "done":
        session.select.stage = Stage.rankSelect.value
        stroke = stroke_sectioner(stroke_pointer("Выбранные жанры:"))
        if len(session.select.gener) == 0:
            for i in Gener:
                session.select.gener.append(i.value)
                stroke += stroke_pointer(i.name)
        else:
            for i in session.select.gener:
                for l in Gener:
                    if l.value == i:
                        stroke += stroke_pointer(l.name)
        markup_clearer(session)
        session.messages_id.append(session.bot.send_message(session.id,stroke).id)
        await asyncio.sleep(1)
        session.message_markup.markup = telebot.types.InlineKeyboardMarkup()
        for i in range(1,6):
            session.message_markup.markup.row(telebot.types.InlineKeyboardButton(f"{i}",callback_data=f"set_{i}"))
        session.message_markup.id = session.bot.send_message(session.id,"Укажите количество 'коленьев'",reply_markup=session.message_markup.markup).id
    else:
        if command.find("gener_add") != -1:
            session.select.gener.append(int(command.split("_")[2]))
        elif command.find("gener_remove") != -1:
            session.select.gener.pop(session.select.gener.index(int(command.split("_")[2])))
        for i in Gener:
            if i.value in session.select.gener:
                session.message_markup.markup.row(
                    telebot.types.InlineKeyboardButton("-",callback_data="none"),
                    telebot.types.InlineKeyboardButton(i.name,callback_data=f"gener_remove_{i.value}")
                )
            else:
                session.message_markup.markup.row(
                    telebot.types.InlineKeyboardButton(i.name,callback_data=f"gener_add_{i.value}"),
                    telebot.types.InlineKeyboardButton("-",callback_data="none")
                )
        session.message_markup.markup.row(
            telebot.types.InlineKeyboardButton("Готово",callback_data="done")
        )
        session.bot.edit_message_text(chat_id=session.id,message_id=session.message_markup.id,text=f"{stroke_sectioner('Список жанров:')}   Неучитываемые:                 Учитываемые:",reply_markup=session.message_markup.markup)
async def functional_result_selecter(session,message):
    if message == "done":
        clear_geter(session)
        session.select_num += 1
        session.selects_store.append(session.select)
        session.select = Select()
        await asyncio.sleep(1)
        session.messages_id.append(session.bot.send_message(session.id,"Запрос отправлен!").id)
    elif message == "cancel":
        return None
async def functional_treshold_selecter(session,message):
    regex_num = re.compile('\d+')
    num = regex_num.findall(message)[0]
    if num != None:
        num = int(num)
        session.select.treshold = num
        session.select.stage = Stage.result.value
        stage_messages_id_clearer(session)
        session.messages_id.append(session.bot.send_message(session.id,stroke_pointer(f"Было указано значение общих фильмов: {num}")).id)
        await asyncio.sleep(1)
        stroke = stroke_sectioner("Итоговый запрос:")
        
        if session.select.target == Target.graf.value:
            stroke += stroke_pointer("Задача: Построение графа;")
        if session.select.type == "act":
            stroke += stroke_pointer("Тип искомой персоны: Актёр;")
        elif session.select.type == "stf":
            stroke += stroke_pointer("Тип искомой персоны: Персонал;")
        stroke += stroke_pointer(f"Ранг: {session.select.rank};")
        stroke += stroke_pointer(f"Порог по общим фильмам: {session.select.treshold};")
        
        stroke += stroke_pointer(f"Искомая персона: {session.select.person.full_name};")
        stroke += stroke_sectioner("Выбранные жанры:")
        for i in Gener:
            if session.select.gener.count(i.value) != 0:
                stroke += stroke_pointer(f"{i.name};")
        
        markup_clearer(session)
        session.message_markup.markup = telebot.types.InlineKeyboardMarkup()
        session.message_markup.markup.row(
            telebot.types.InlineKeyboardButton("Принять",callback_data="done"),
            telebot.types.InlineKeyboardButton("Отмена",callback_data="cancel")
        )
        
        session.message_markup.id = session.bot.send_message(session.id,stroke,reply_markup=session.message_markup.markup).id
        session.select.target = None
    else:
        session.stage_messages_id.append(session.bot.send_message(session.id,"Ввод не корректен! Попробуйте повторить попытку."))
    return None
async def functional_end_year_selecter(bot,message):
    return None
async def functional_start_year_selecter(bot,message):
    return None