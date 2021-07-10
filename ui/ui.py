import telebot
import asyncio
from enum import Enum, auto
from db.DBHolder import DBHolder
from models.dataclasses.Params import Params
from models.dataclasses.User import User
from models.enums.UserType import UserType

from controller.controller import KinopoiskBotController
from network.NetworkModule import NetworkModule


def print_hello():
    print('Hello')


KinopoiskBotController.init()
with open('security.txt', 'r') as fp:
    data = fp.read()
    token = data.split("\n")[0].split("=")[1]
bot = telebot.TeleBot(token)
print('Bot has been launched')


def stroke_pointer(stroke, point="*"):
    return f"{point} {stroke}\n"


def stroke_sectioner(stroke, point=""):
    if point != "":
        point += " "
    return f"{point}{stroke}\n-----\n"


# class User:
#     def __init__(self, id, type, name):
#         if type == "usu" or type == "adm" or type == "bos":
#             self.id = id
#             self.type = type
#             self.name = name
#             self.last_date_use = date.today()
#             self.start_date_use = date.today()
#         else:
#             print("* err - Был указан несуществующий тип пользователя;")
#
#
# class Parms:
#     def __init__(self):
#         self.name = None
#         self.rank = None
#         self.step = None
#         self.geners = []
#         self.threshold = None
#         self.end_year = None
#         self.is_actors = None
#         self.person_id = None
#         self.start_year = None
#         self.generate_gif = None
#
#
# class Person:
#     def __init__(self, person_id, person_type, full_name, positions, start_year, end_year, photo_url):
#         self.person_id = person_id
#         self.full_name = full_name
#         self.positions = positions
#         self.start_year = start_year
#         self.end_year = end_year
#         self.photo_url = photo_url


class Session:
    count = 0
    bos_session = []
    adm_session = []
    usu_session = []
    bos_id_list = [632012083, 1170650256, 426134463]
    adm_id_list = [361877365, 1839000131]

    def __init__(self, id, bot, name, intro):
        self.id = id
        self.bot = bot
        self.user = None
        self.store = []
        self.stage = None
        self.parms = Params()
        self.target = None
        self.favs = []
        self.messages = Messages(self)
        self.stage_path = []
        Session.count += 1
        stroke = ""
        for i in Session.bos_id_list:
            if i == id:
                self.user = User(id, name, UserType.root)
                Session.bos_session.append(self)
                stroke = "Добро пожаловать, уважаемый руководитель!"
        if self.user == None:
            for i in Session.adm_id_list:
                if i == id:
                    self.user = User(id, name, UserType.admin)
                    Session.adm_session.append(self)
                    stroke = "Добро пожаловать, уважаемый администратор!"
        if self.user is None:
            self.user = User(id, name, UserType.plain_user)
            Session.usu_session.append(self)
            stroke = "Добро пожаловать, уважаемый пользователь!"
        KinopoiskBotController.add_user(user=self.user)
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

    def pauser(self, sec=1):
        asyncio.run(self.messages.pauser(sec=sec))


class Messages:
    row_date = 5
    row_list = 15
    column_date = 6
    year_begin = 1920

    def __init__(self, session):
        self.id = None
        self.info = []
        self.help = []
        self.index = None
        self.callback = None
        self.progress = None
        self.parms = Params()
        self.markup = []
        self.session = session
        self.stage_list = []
        self.other_list = []
        self.target_list = []

    async def pauser(self, sec=1):
        await asyncio.sleep(sec)

    def clear(self):
        if self.id != None:
            self.message_deleter(self.id)
        self.help_clear()
        self.markup_clear()

    def all_clear(self):
        return None

    def favs_info_geter(self, id):
        parms = self.session.favs[id]
        stroke = stroke_sectioner("Выбранный запрос:")
        if parms.generate_gif == True:
            stroke += stroke_pointer(f"Функционал: построение хронологии;", "✫")
        else:
            stroke += stroke_pointer(f"Функционал: построение графа;", "✫")
        stroke += stroke_pointer(f"Искомая персона: {parms.person.full_name};", "✫")
        if parms.actors_only:
            stroke += stroke_pointer(f"Тип искомой персоны: актёр;", "✫")
        else:
            stroke += stroke_pointer(f"Тип искомой персоны: персонал;", "✫")
        if parms.start_year != None:
            stroke += stroke_pointer(f"Начало периода: {parms.start_year};", "✫")
        if parms.end_year != None:
            stroke += stroke_pointer(f"Конец периода: {parms.end_year};", "✫")
        if parms.step != None:
            stroke += stroke_pointer(f"Значения отрезков: {parms.step};", "✫")
        stroke += stroke_pointer(f"Глубина построения связи: {parms.rank};", "✫")
        stroke += stroke_pointer(f"Минимальное количество общих фильмов: {parms.threshold};", "✫")
        stroke += stroke_sectioner(f"Жанры:", "✫")
        for i in DBHolder.get_genres_with_ids():
            if parms.genres.count(i[0]) > 0:
                stroke += stroke_pointer(i[1])
        self.info_clear()
        markup = self.markup_geter()
        markup.row(self.markup_button_geter("Повторить", f"favs_repeat_{id}"))
        markup.row(self.markup_button_geter("Убрать", f"favs_fair_{id}"))
        self.info.append(self.markup_sender(stroke, markup))

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
        self.session.parms = Params()

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
        self.markup.append(
            self.markup_sender("Какой функционал приложения вы желаете задействовать?", self.get_func_markuper()))

    def help_geter(self):
        self.help_clear()
        if self.session.user.user_type == UserType.root:
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
                stroke_pointer(
                    "Сделать пользователя администратором можно с помощью команды `assign_adm id` (где id - это ID пользователя в Телеграмме) или выбрав соответсвующий пункт в информации пользователя.") +
                stroke_pointer(
                    "Снять администратора с должности можно с помощью команды `fire_adm id` (где id - это ID пользователя в Телеграмме) или выбрав соответсвующий пункт в информации пользователя.")
            )
        if self.session.user.user_type == UserType.admin:
            self.help_message_sender(
                stroke_sectioner(
                    "Здесь вы можете ознакомиться с полным списком команд, для продвинутого взаимодействия с ботом:") +
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
        self.markup_clear()
        self.session.target = None
        self.parms_clear()
        self.index = 0
        history = KinopoiskBotController.get_history(self.session.user)
        self.session.store = [e.params for e in history]
        self.markup.append(self.markup_sender(f"Список запросов:", self.markup_list_geter(self.session.store, "store")))

    def users_geter(self):
        self.markup_clear()
        if len(Session.usu_session) > 0:
            self.markup.append(
                self.markup_sender("Список пользователей:", self.markup_list_geter(Session.usu_session, "usu")))
        else:
            self.other_message_sender("Список пользователей пуст!")

    def admins_geter(self):
        self.markup_clear()
        if len(Session.adm_session) > 0:
            self.markup.append(
                self.markup_sender("Список администраторов:", self.markup_list_geter(Session.adm_session, "adm")))
        else:
            self.other_message_sender("Список администраторов пуст!")

    def person_geter(self, id):
        res = []
        person = None
        for i in self.session.parms.person_id:
            if i.person_id == id:
                person = i
                break
        res.append(self.send_photo_url(person.url))
        res.append(
            self.message_sender(f"Имя: {person.full_name};"))
        return res

    def usu_info_geter(self, id):
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
                markup.row(self.markup_button_geter("Выдать права администратора", f"assign_adm_{usu.id}"))
                self.info.append(self.markup_sender(stroke, markup))
                return None
            elif usu.type == "adm":
                markup = self.markup_geter()
                markup.row(self.markup_button_geter("Лишить прав администратора", f"fire_adm_{usu.id}"))
                self.info.append(self.markup_sender(stroke, markup))

    def store_info_geter(self, id):
        parms = self.session.store[id]
        stroke = stroke_sectioner("Выбранный запрос:")
        if parms.generate_gif == True:
            stroke += stroke_pointer(f"Функционал: построение хронологии;", "✫")
        else:
            stroke += stroke_pointer(f"Функционал: построение графа;", "✫")
        stroke += stroke_pointer(f"Искомая персона: {parms.person.full_name};", "✫")
        if parms.actors_only:
            stroke += stroke_pointer(f"Тип искомой персоны: актёр;", "✫")
        else:
            stroke += stroke_pointer(f"Тип искомой персоны: персонал;", "✫")
        if parms.start_year != None:
            stroke += stroke_pointer(f"Начало периода: {parms.start_year};", "✫")
        if parms.end_year != None:
            stroke += stroke_pointer(f"Конец периода: {parms.end_year};", "✫")
        if parms.step != None:
            stroke += stroke_pointer(f"Значения отрезков: {parms.step};", "✫")
        stroke += stroke_pointer(f"Глубина построения связи: {parms.rank};", "✫")
        stroke += stroke_pointer(f"Минимальное количество общих фильмов: {parms.threshold};", "✫")
        stroke += stroke_sectioner(f"Жанры:", "✫")
        for i in DBHolder.get_genres_with_ids():
            if parms.genres.count(i[0]) > 0:
                stroke += stroke_pointer(i[1])
        self.markup_clear()
        markup = self.markup_geter()
        markup.row(self.markup_button_geter("Повторить", f"store_repeat_{id}"))
        markup.row(self.markup_button_geter("Избрать", f"store_choose_{id}"))
        self.markup.append(self.markup_sender(stroke, markup))

    def markup_list_geter(self, arg_list, prefix):
        self.list = arg_list
        markup = self.markup_geter()
        arg_list_len = len(arg_list)
        if arg_list_len > 0:
            for i in range(self.index, self.index + Messages.row_list):
                text = ""
                callback = ""
                if i <= arg_list_len - 1:
                    if prefix == "usu":
                        text = f"№{'0' * (4 - len(str(i)))}{i} - Имя: {arg_list[i].user.name};"
                        callback = f"{prefix}_set_{Session.usu_session[i].id}"
                    elif prefix == "adm":
                        text = f"№{'0' * (4 - len(str(i)))}{i} - Имя: {arg_list[i].user.name};"
                        callback = f"{prefix}_set_{Session.adm_session[i].id}"
                    elif prefix == "store":
                        typ = None
                        if arg_list[i].generate_gif:
                            typ = "cron"
                        else:
                            typ = "graf"
                        text = f"Тип: {typ}, Персона: {arg_list[i].person.full_name}"
                        callback = f"{prefix}_set_{i}"
                    elif prefix == "favs":
                        typ = None
                        if arg_list[i].generate_gif:
                            typ = "cron"
                        else:
                            typ = "graf"
                        text = f"Тип: {typ}, Персона: {arg_list[i].person.full_name}"
                        callback = f"{prefix}_set_{i}"
                else:
                    text = "-"
                    callback = "none"
                markup.row(self.markup_button_geter(text, callback))
            markup.row(
                self.markup_button_geter("⮝", f"{prefix}_up"),
                self.markup_button_geter("⮟", f"{prefix}_down")
            )
            return markup

    def markup_button_geter(self, arg_text, callback):
        return telebot.types.InlineKeyboardButton(text=arg_text, callback_data=callback)

    def adm_firer(self, id):
        session = Session.finder(id)
        Session.adm_session.remove(session)
        Session.usu_session.append(session)
        session.user.type = "usu"
        self.markup_clear()
        if len(Session.adm_session) > 0:
            self.admins_geter()
        self.usu_info_geter(id)

    def adm_assigner(self, id):
        session = Session.finder(id)
        Session.usu_session.remove(session)
        Session.adm_session.append(session)
        session.user.type = "adm"
        self.markup_clear()
        self.users_geter()
        self.usu_info_geter(id)

    def parms_favner(self, id):
        params = self.session.store[id]
        try:
            i = params.person.person_id
        except:
            params.person = NetworkModule.get_person_by_id(params.person)
        KinopoiskBotController.add_fav(params, self.session.id)
        self.session.favs.append(params)
        self.markup_clear()
        self.store_geter()
        self.info_clear()

    def parms_refavner(self, id):
        params = self.session.favs.pop(id)
        KinopoiskBotController.remove_fav(params, self.session.id)
        self.markup_clear()
        self.info_clear()
        self.favs_geter()

    def parms_repeater(self, id):
        self.session.parms = self.session.store[id]
        self.worker()

    def favs_repeater(self, id):
        self.session.parms = self.session.favs[id]
        self.worker()

    def favs_geter(self):
        self.markup_clear()
        self.info_clear()
        self.session.target = None
        self.parms_clear()
        self.index = 0
        self.session.favs = KinopoiskBotController.get_favorites(self.session.user)
        if len(self.session.favs) > 0:
            self.markup.append(
                self.markup_sender(f"Список избранных:", self.markup_list_geter(self.session.favs, "favs")))

    def markup_geter(self):
        return telebot.types.InlineKeyboardMarkup()

    def markup_sender(self, text, markup):
        return self.session.bot.send_message(self.session.id, text, reply_markup=markup).id

    def markup_editer(self, arg_text, markup):
        self.session.bot.edit_message_text(chat_id=self.session.id, message_id=self.markup[0], text=arg_text,
                                           reply_markup=markup)

    def markup_num_geter(self):
        markup = self.markup_geter()
        markup.row(
            self.markup_button_geter("-10", "inc_10"),
            self.markup_button_geter("-5", "inc_5"),
            self.markup_button_geter("-1", "inc_1"),
            self.markup_button_geter("+1", "add_1"),
            self.markup_button_geter("+5", "add_5"),
            self.markup_button_geter("+10", "add_10")
        )
        markup.row(
            self.markup_button_geter("Принять", "done")
        )
        return markup

    def get_func_markuper(self):
        markup = self.markup_geter()
        markup.row(self.markup_button_geter("Получить граф связей кино-персоны", "graf"))
        markup.row(self.markup_button_geter("Получить хронологию кино-персоны", "cron"))
        return markup

    def markup_date_geter(self):
        markup = self.markup_geter()
        index = Messages.year_begin + self.index
        for count1 in range(Messages.row_date):
            row = []
            count = 0
            for count2 in range(index, index + Messages.column_date):
                row.append(self.markup_button_geter(f"{count2}", f"set_{count2}"))
                count += 1
            markup.row().keyboard.append(row)
            index += count
        markup.row(
            self.markup_button_geter("⮜", "left"),
            self.markup_button_geter("⮞", "right")
        )
        return markup

    def markup_list_changer(self, id, arg_list, prefix):
        if prefix == "adm" or prefix == "usu":
            self.usu_info_geter(id)
        elif prefix == "store":
            self.store_info_geter(id)

    def markup_list_rechanger(self, text, direct, arg_list, prefix):
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
        markup = self.markup_list_geter(arg_list, prefix)
        self.markup_editer(text, markup)

    def message_deleter(self, id):
        self.session.bot.delete_message(self.session.id, id)

    def send_photo_url(self, url):
        url = url.split('//')[1]
        return self.session.bot.send_photo(self.session.id, url).id

    def send_photo_path(self, path):
        return self.session.bot.send_photo(self.session.id, open(path, "rb")).id

    def message_sender(self, text):
        return self.session.bot.send_message(self.session.id, text).id

    def message_editer(self, id, arg_text):
        self.session.bot.edit_message_text(chat_id=self.session.id, message_id=id, text=arg_text)

    def info_message_sender(self, text):
        self.info.append(self.message_sender(text))

    def help_message_sender(self, text):
        self.help.append(self.message_sender(text))

    def stage_massage_sender(self, text):
        self.stage_list.append(self.session.bot.send_message(self.session.id, text).id)

    def other_message_sender(self, text):
        self.other_list.append(self.session.bot.send_message(self.session.id, text).id)

    def target_message_sender(self, text):
        self.target_list.append(self.session.bot.send_message(self.session.id, text).id)

    def graf_targer(self, callback):
        self.callback = callback
        if self.session.target == None:
            self.parms_clear()
            self.markup_clear()
            self.session.stage_path = [
                Stage.typeSelect.value,
                Stage.nameSelect.value,
                Stage.idSelect.value,
                Stage.generSelect.value,
                Stage.thresholdSelect.value,
                Stage.rankSelect.value,
                Stage.result.value
            ]
            self.target_message_sender(stroke_pointer("Был указан функционал: построение графа;", "✫"))
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
        if self.session.stage == Stage.generSelect.value:
            self.gener_supplicanter()
        if self.session.stage == Stage.thresholdSelect.value:
            self.threshold_supplicanter()
        if self.session.stage == Stage.rankSelect.value:
            self.rank_supplicanter()
        if self.session.stage == Stage.result.value:
            self.result_supplicanter()

    def cron_targer(self, callback):
        self.callback = callback
        if self.session.target == None:
            self.parms_clear()
            self.markup_clear()
            self.session.stage_path = [
                Stage.typeSelect.value,
                Stage.nameSelect.value,
                Stage.idSelect.value,
                Stage.startYearSelect.value,
                Stage.endYearSelect.value,
                Stage.stepSelect.value,
                Stage.generSelect.value,
                Stage.thresholdSelect.value,
                Stage.rankSelect.value,
                Stage.result.value
            ]
            self.target_message_sender(stroke_pointer("Был указан функционал: построение хронологии;", "✫"))
            self.session.target = Target.cron.value
            self.session.parms.generate_gif = True
            self.session.stage = self.session.stage_path.pop(0)
            self.callback = "begin"
            self.session.pauser()
        if self.session.stage == Stage.typeSelect.value:
            self.type_supplicanter()
        if self.session.stage == Stage.nameSelect.value:
            self.name_supplicanter()
        if self.session.stage == Stage.idSelect.value:
            self.id_supplicanter()
        if self.session.stage == Stage.startYearSelect.value:
            self.start_year_supplicanter()
        if self.session.stage == Stage.endYearSelect.value:
            self.end_year_supplicanter()
        if self.session.stage == Stage.stepSelect.value:
            self.step_supplicanter()
        if self.session.stage == Stage.generSelect.value:
            self.gener_supplicanter()
        if self.session.stage == Stage.thresholdSelect.value:
            self.threshold_supplicanter()
        if self.session.stage == Stage.rankSelect.value:
            self.rank_supplicanter()
        if self.session.stage == Stage.result.value:
            self.result_supplicanter()

    def id_supplicanter(self):
        if self.callback == "begin":
            self.session.pauser()
            for i in range(len(self.session.parms.person_id)):
                person = self.session.parms.person_id[i]
                markup = self.markup_geter()
                markup.row(self.markup_button_geter("Выбрать", f"set_pers_{person.person_id}"))
                if person.url is None:
                    person.url = 'https://www.yildizgaz.com.tr/Assets/images/no-img.jpg'
                self.markup.append(self.send_photo_url(person.url))
                self.markup.append(self.markup_sender(
                    f"Имя: {person.full_name};", markup))
        elif self.callback.find("set_pers") != -1:
            self.markup_clear()
            self.stage_message_clear()
            person = None
            index = int(self.callback.split("_")[2])
            for i in self.session.parms.person_id:
                if i.person_id == index:
                    person = i
            self.session.parms.name = person.full_name
            self.session.parms.person_id = person.person_id
            self.target_message_sender(stroke_pointer("Была указана кино-персона:", "✫"))
            self.target_list.extend(self.person_geter(person.person_id))
            self.session.stage = self.session.stage_path.pop(0)
            self.callback = "begin"

    def type_supplicanter(self):
        if self.callback == "begin":
            self.markup_clear()
            markup = self.markup_geter()
            markup.row(
                self.markup_button_geter("Персонал", "stf"),
                self.markup_button_geter("Актёр", "act")
            )
            self.markup.append(self.markup_sender("Укажите тип кино-персоны, которую необходимо найти:", markup))
        if self.callback == "stf" or self.callback == "act":
            if self.callback == "stf":
                self.markup_clear()
                self.session.parms.actors_only = False
                self.target_message_sender(stroke_pointer("Был указан тип кино-персоны: персонал;", "✫"))
            elif self.callback == "act":
                self.markup_clear()
                self.session.parms.actors_only = True
                self.target_message_sender(stroke_pointer("Был указан тип кино-персоны: актёр;", "✫"))
            self.callback = "begin"
            self.session.stage = self.session.stage_path.pop(0)

    def name_supplicanter(self):
        if self.callback == "begin":
            self.session.pauser()
            self.stage_massage_sender("Укажите полное имя искомой персоны:")
        else:
            person_list = NetworkModule.get_actors(self.callback)
            self.session.parms.person_id = []
            for i in person_list:
                if i.full_name.lower() == self.callback.lower():
                    self.session.parms.person_id.append(i)
            len_list = len(self.session.parms.person_id)
            if len_list > 1:
                self.stage_massage_sender("Найдено множество соответсвий:")
                self.session.stage = self.session.stage_path.pop(0)
            elif len_list == 1:
                # self.session.parms.person_id = self.session.parms.person_id[0]
                person = self.session.parms.person_id[0]
                self.target_message_sender("Найдено однозначное соответствие:")
                self.session.stage_path.pop(0)
                self.session.stage = self.session.stage_path.pop(0)
                self.session.pauser()
                self.person_geter(person.person_id)
                self.session.parms.name = person.full_name
                self.session.parms.person_id = person.person_id
                self.callback = "begin"
            elif len_list == 0:
                self.target_message_sender("Соответствий не найдено!")
                self.session.pauser()
                self.target_message_sender("Попробуйте повторить попытку.")
            self.callback = "begin"

    def step_supplicanter(self):
        if self.callback == "begin":
            self.markup_clear()
            self.index = 1
            self.markup.append(
                self.markup_sender(f"Укажите шаг продвижения по периоду: {self.index}", self.markup_num_geter()))
        elif self.callback.find("add") != -1 or \
                self.callback.find("inc") != -1:
            num = int(self.callback.split("_")[1])
            if self.callback.find("add") != -1:
                self.index += num
            elif self.callback.find("inc") != -1:
                self.index -= num
                if self.index <= 0:
                    self.index += num
                    return None
            self.markup_editer(f"Укажите шаг продвижения по периоду: {self.index}", self.markup_num_geter())
        elif self.callback == "done":
            self.callback = "begin"
            self.session.parms.step = self.index
            self.index = None
            self.session.stage = self.session.stage_path.pop(0)
            self.markup_clear()
            self.target_message_sender(
                stroke_pointer(f"Был указан шаг продвижения по периоду: {self.session.parms.step};", "✫"))
            self.callback = "begin"
            self.session.pauser()

    def rank_supplicanter(self):
        if self.callback == "begin":
            self.stage_message_clear()
            self.markup_clear()
            self.stage_massage_sender(
                "Глубина построения связи позволяет продолжить формирование сети по отобранным ранее актёрам. При значении равном '1' мы получим только самого актёра, для '2' будут получены контакты с данной персоной, а для '3' - контакты их контактов. Рекомендуем вам проверить это на практике!")
            self.session.pauser()
            self.index = 1
            self.markup.append(
                self.markup_sender(f"Укажите глубину построения связи: {self.index}", self.markup_num_geter()))
        elif self.callback.find("add") != -1 or \
                self.callback.find("inc") != -1:
            num = int(self.callback.split("_")[1])
            if self.callback.find("add") != -1:
                self.index += num
            elif self.callback.find("inc") != -1:
                self.index -= num
                if self.index <= 0:
                    self.index += num
                    return None
            self.markup_editer(f"Укажите глубину построения связи: {self.index}", self.markup_num_geter())
        elif self.callback == "done":
            self.callback = "begin"
            self.session.parms.rank = self.index
            self.index = None
            self.session.stage = self.session.stage_path.pop(0)
            self.markup_clear()
            self.target_message_sender(
                stroke_pointer(f"Была указана глубина построения связи: {self.session.parms.rank}", "✫"))
            self.session.pauser()

    def gener_supplicanter(self):
        if self.callback == "begin":
            self.session.pauser()
            self.stage_message_clear()
            self.markup_clear()
            markup = self.markup_geter()
            for i in DBHolder.get_genres_with_ids():
                markup.row(
                    self.markup_button_geter(f"{i[1]}", f"gener_add_{i[0]}"),
                    self.markup_button_geter("-", "none")
                )
            markup.row(self.markup_button_geter("Принять", "done"))
            self.markup.append(self.markup_sender("Укажите допустимые жанры:", markup))
            self.stage_massage_sender(
                stroke_pointer("Выбранные Вами жанры будут перемещены и расположены в правой части панели;") +
                stroke_pointer("Жанры, оставшиеся слева будут отфильтрованы;") +
                stroke_pointer("Если не будет указан ни один жанр из списка, то будут выбраны все жанры;")
            )
        elif self.callback.find("gener_add") != -1 or self.callback.find("gener_remove") != -1:
            index = int(self.callback.split("_")[2])
            markup = self.markup_geter()
            if self.callback.find("gener_add") != -1:
                self.session.parms.genres.append(index)
            elif self.callback.find("gener_remove") != -1:
                self.session.parms.genres.remove(index)
            for i in DBHolder.get_genres_with_ids():
                if i[0] in self.session.parms.genres:
                    markup.row(
                        self.markup_button_geter("-", "none"),
                        self.markup_button_geter(i[1], f"gener_remove_{i[0]}")
                    )
                else:
                    markup.row(
                        self.markup_button_geter(i[1], f"gener_add_{i[0]}"),
                        self.markup_button_geter("-", "none")
                    )
            markup.row(self.markup_button_geter("Принять", "done"))
            self.markup_editer("Укажите допустимые жанры:", markup)
        elif self.callback == "done":
            stroke = stroke_sectioner("Указанные жанры:", "✫")
            if len(self.session.parms.genres) > 0:
                for i in DBHolder.get_genres_with_ids():
                    if i[0] in self.session.parms.genres:
                        stroke += stroke_pointer(i)
            else:
                self.session.parms.genres = []
                # for i in DBHolder.get_genres():
                #     self.session.parms.genres.append(i)
                #     stroke += stroke_pointer(i)
            self.markup_clear()
            self.stage_message_clear()
            self.target_message_sender(stroke)
            self.callback = "begin"
            self.session.stage = self.session.stage_path.pop(0)

    def result_supplicanter(self):
        if self.callback == "begin":
            self.markup_clear()
            self.stage_message_clear()
            self.target_message_clear()
            self.index = None
            stroke = stroke_sectioner("Итоговый запрос:")
            if self.session.parms.generate_gif == True:
                stroke += stroke_pointer(f"Функционал: построение хронологии;", "✫")
            else:
                stroke += stroke_pointer(f"Функционал: построение графа;", "✫")
            stroke += stroke_pointer(f"Искомая персона: {self.session.parms.name};", "✫")
            if self.session.parms.actors_only:
                stroke += stroke_pointer(f"Тип искомой персоны: актёр;", "✫")
            else:
                stroke += stroke_pointer(f"Тип искомой персоны: персонал;", "✫")
            if self.session.parms.start_year != None:
                stroke += stroke_pointer(f"Начало периода: {self.session.parms.start_year};", "✫")
            if self.session.parms.end_year != None:
                stroke += stroke_pointer(f"Конец периода: {self.session.parms.end_year};", "✫")
            if self.session.parms.step != None:
                stroke += stroke_pointer(f"Значения отрезков: {self.session.parms.step};", "✫")
            stroke += stroke_pointer(f"Глубина построения связи: {self.session.parms.rank};", "✫")
            stroke += stroke_pointer(f"Минимальное количество общих фильмов: {self.session.parms.threshold};", "✫")
            stroke += stroke_sectioner(f"Жанры:", "✫")
            for i in DBHolder.get_genres_with_ids():
                if self.session.parms.genres.count(i[0]) > 0:
                    stroke += stroke_pointer(i[1])
            markup = self.markup_geter()
            markup.row(
                self.markup_button_geter("Принять", "done"),
                self.markup_button_geter("Отменить", "cancel")
            )
            self.markup.append(self.markup_sender(stroke, markup))
        elif self.callback == "done":
            progress = Progress_bar()
            self.progress = self.message_sender(progress.bar)
            result = self.worker()
            params = self.session.parms.person_id
            # params.person = self.session.parms.person_id
            self.session.store.append(params)
            self.parms_clear()
            self.markup_clear()
            self.session.target = None
            self.other_message_sender("Запрос отправлен!")
            self.session.pauser()
        elif self.callback == "cancel":
            self.parms_clear()
            self.markup_clear()
            self.session.target = None
            self.other_message_sender("Запрос отменен!")

    def end_year_supplicanter(self):
        if self.callback == "begin":
            self.stage_message_clear()
            self.markup_clear()
            self.index = 0
            self.markup.append(self.markup_sender("Укажите конец периода:", self.markup_date_geter()))
        elif self.callback == "left" or self.callback == "right":
            bias = Messages.row_date * Messages.column_date
            if self.callback == "left":
                self.index -= bias
                if self.index + Messages.year_begin < Messages.year_begin:
                    self.index += bias
                    return None
            elif self.callback == "right":
                self.index += bias
            self.markup_editer("Укажите конец периода:", self.markup_date_geter())
        elif self.callback.find("set") != -1:
            if self.session.parms.start_year > int(self.callback.split("_")[1]):
                return None
            self.markup_clear()
            self.session.parms.end_year = int(self.callback.split("_")[1])
            self.target_message_sender(stroke_pointer(f"Был указан конец периода: {self.session.parms.end_year};", "✫"))
            self.session.stage = self.session.stage_path.pop(0)
            self.callback = "begin"

    def threshold_supplicanter(self):
        if self.callback == "begin":
            self.index = 1
            self.markup_clear()
            markup = self.markup_num_geter()
            self.session.pauser()
            self.markup.append(self.markup_sender(
                f"Укажите минимальное число общих фильмов данной персоны с другими кино-персонами: {self.index}",
                markup))
        elif self.callback.find("add") != -1 or \
                self.callback.find("inc") != -1:
            num = int(self.callback.split("_")[1])
            if self.callback.find("add") != -1:
                self.index += num
            elif self.callback.find("inc") != -1:
                self.index -= num
                if self.index <= 0:
                    self.index += num
                    return None
            self.markup_editer(
                f"Укажите минимальное число общих фильмов данной персоны с другими кино-персонами: {self.index}",
                self.markup_num_geter())
        elif self.callback == "done":
            self.callback = "begin"
            self.session.parms.threshold = self.index
            self.index = None
            self.session.stage = self.session.stage_path.pop(0)
            self.markup_clear()
            self.target_message_sender(
                stroke_pointer(f"Было указано пороговое значение общих фильмов: {self.session.parms.threshold}", "✫"))
            self.session.pauser()

    def start_year_supplicanter(self):
        if self.callback == "begin":
            self.stage_message_clear()
            self.markup_clear()
            self.index = 0
            self.markup.append(self.markup_sender("Укажите начало периода:", self.markup_date_geter()))
        elif self.callback == "left" or self.callback == "right":
            bias = Messages.row_date * Messages.column_date
            if self.callback == "left":
                self.index -= bias
                if self.index + Messages.year_begin < Messages.year_begin:
                    self.index += bias
                    return None
            elif self.callback == "right":
                self.index += bias
            self.markup_editer("Укажите начало периода:", self.markup_date_geter())
        elif self.callback.find("set") != -1:
            self.markup_clear()
            self.session.parms.start_year = int(self.callback.split("_")[1])
            self.target_message_sender(
                stroke_pointer(f"Было указано начало периода: {self.session.parms.start_year};", "✫"))
            self.session.stage = self.session.stage_path.pop(0)
            self.callback = "begin"

    def worker(self):
        params = self.session.parms
        try:
            i = params.person.person_id
        except:
            params.person = NetworkModule.get_person_by_id(params.person_id)
        result = KinopoiskBotController.get_graph(self.session.parms, self.progress, self.session.id)
        if not params.generate_gif:
            self.other_message_sender("Результат:")
            self.other_list.append(self.send_photo_path(result.path))
        if params.generate_gif:
            self.other_message_sender("Результат:")
            self.other_list.append(self.session.bot.send_animation(self.session.id, result.path).id)
        return result


class Progress_bar:
    void = "▒"
    point = "█"
    left_limit = "﴾"
    right_limit = "﴿"
    progress_point = 10
    progress_procent = 100

    def __init__(self, id=None, chat_id=None):
        self.id = None
        self.bot = bot
        self.point = 0
        self.chat_id = chat_id
        self.progress = 0
        self.bar = f"{Progress_bar.left_limit}{Progress_bar.point * self.point}{Progress_bar.void * (Progress_bar.progress_point - self.point)}{Progress_bar.right_limit}{self.progress}%"

    def progresser(self):
        self.bar = f"{Progress_bar.left_limit}{Progress_bar.point * self.point}{Progress_bar.void * (Progress_bar.progress_point - self.point)}{Progress_bar.right_limit}{self.progress}%"

    def adder(self, add=1):
        for i in range(add):
            self.progress += 1
            if self.progress > 100:
                break
            if self.progress % (
                    Progress_bar.progress_procent / Progress_bar.progress_point) == 0 and self.progress != 0:
                self.point += 1
        self.progresser()
        self.bot.edit_message_text(chat_id=self.chat_id, message_id=self.id, text=self.bar)

    def ender(self):
        self.adder(add=100 - self.progress)


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


class Target(Enum):
    graf = auto()
    cron = auto()
    persons = auto()
    person_films = auto()


@bot.callback_query_handler(func=lambda call: True)
def call_determenant(call):
    id = call.message.chat.id
    print(f'act from #{id}')
    text = call.data
    session = Session.finder(id)

    if session.target == Target.graf.value or session.target == Target.cron.value:
        if session.target == Target.graf.value:
            if text == "act" or \
                    text == "stf" or \
                    text == "done" or \
                    text == "cancel" or \
                    text.find("add") != -1 or \
                    text.find("inc") != -1 or \
                    text.find("set_pers") != -1 or \
                    text.find("gener_add") != -1 or \
                    text.find("gener_remove") != -1:
                session.messages.graf_targer(text)
        if session.target == Target.cron.value:
            if text == "act" or \
                    text == "stf" or \
                    text == "left" or \
                    text == "right" or \
                    text == "done" or \
                    text == "cancel" or \
                    text.find("add") != -1 or \
                    text.find("inc") != -1 or \
                    text.find("set") != -1 or \
                    text.find("set_pers") != -1 or \
                    text.find("gener_add") != -1 or \
                    text.find("gener_remove") != -1:
                session.messages.cron_targer(text)

    if text == "graf":
        session.target = None
        session.stage = None
        session.messages.parms_clear()
        session.messages.graf_targer(text)
    if text == "cron":
        session.target = None
        session.stage = None
        session.messages.parms_clear()
        session.messages.cron_targer(text)
    elif text == "usu_up":
        session.messages.markup_list_rechanger("Список пользователей:", True, Session.usu_session, "usu")
    elif text == "adm_up":
        session.messages.markup_list_rechanger("Список администратор:", True, Session.usu_session, "adm")
    elif text == "favs_up":
        return None
    elif text == "usu_down":
        session.messages.markup_list_rechanger("Список пользователей:", False, Session.usu_session, "usu")
    elif text == "adm_down":
        session.messages.markup_list_rechanger("Список администратор:", False, Session.usu_session, "adm")
    elif text == "store_up":
        session.messages.markup_list_rechanger("Список запросов:", True, session.store, "store")
    elif text == "favs_down":
        return None
    elif text == "store down":
        session.messages.markup_list_rechanger("Список запросов:", False, session.store, "store")
    elif text.find("usu_set") != -1:
        session.messages.markup_list_changer(int(text.split("_")[2]), Session.usu_session, "usu")
    elif text.find("adm_set") != -1:
        session.messages.markup_list_changer(int(text.split("_")[2]), Session.adm_session, "adm")
    elif text.find("fire_adm") != -1:
        session.messages.adm_firer(int(text.split("_")[2]))
    elif text.find("favs_set") != -1:
        session.messages.favs_info_geter(int(text.split("_")[2]))
    elif text.find("favs_fair") != -1:
        session.messages.parms_refavner(int(text.split("_")[2]))
    elif text.find("store_set") != -1:
        session.messages.markup_list_changer(int(text.split("_")[2]), session.store, "store")
    elif text.find("assign_adm") != -1:
        session.messages.adm_assigner(int(text.split("_")[2]))
    elif text.find("store_choose") != -1:
        session.messages.parms_favner(int(text.split("_")[2]))
    elif text.find("store_repeat") != -1:
        session.messages.parms_repeater(int(text.split("_")[2]))
    elif text.find("favs_repeat") != -1:
        session.messages.favs_repeater(int(text.split("_")[2]))



@bot.message_handler(commands=[
    "id",
    "func",
    "help",
    "store",
    "clear",
    "get_users",
    "get_admins",
    'favs'])
def command_handler(message):
    id = message.chat.id
    text = message.text
    session = Session.finder(id)
    if session != None:
        if session.user.user_type.value != 0:
            if text == "/get_users":
                session.messages.index = 0
                session.messages.users_geter()
            if session.user.user_type.value != 1:
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
        elif text == "/favs":
            session.messages.favs_geter()
        elif text == "/store":
            session.messages.store_geter()

    else:
        print("GG")


@bot.message_handler(content_types=["text"])
def message_handler(message):
    id = message.chat.id
    text = message.text
    name = message.from_user.username
    session = Session.finder(id)
    if session != None:
        if session.target == Target.graf.value or session.target == Target.cron.value:
            if session.target == Target.graf.value:
                if session.stage == Stage.nameSelect.value:
                    session.messages.graf_targer(text)
            elif session.target == Target.cron.value:
                if session.stage == Stage.nameSelect.value:
                    session.messages.cron_targer(text)
    else:
        session = Session(id, bot, name, True)


bot.polling(none_stop=True)
