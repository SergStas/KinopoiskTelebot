import db.DBWork
import db.DBWork as bd
from db import DBWork
from db.DBHolder import DBHolder as holder
from models.dataclasses.Params import Params
from models.dataclasses.Person import Person
from models.dataclasses.Relation import Relation
from models.dataclasses.User import User
from models.enums.Genre import Genre
from models.enums.Position import Position
from models.enums.UserType import UserType


class Req:
    def __init__(self, user_id, params):
        self.user_id = user_id
        self.params = params


def print_hi(name):
    print(f'Hi, {name}')
    bd.start_bd()

    a = Person(0, 'Well Smooth', [Position.actor, Position.other], 1980, 2020, 'sfdg')
    b = Person(20, 'Samuel Ponk', [Position.actor], 1990, 2021, 'sfdg')
    c = Person(4, 'Ben Cam', [Position.other], 2010, 2021, 'sfdg')
    d = Person(1, 'Jim Foos', [Position.other, Position.actor], 1990, 2021, 'sfdg')
    e = Person(5, 'Cole Berne', [Position.actor], 1986, 2021, 'sfdg')
    f = Person(7, 'Monk Zigh', [Position.actor, Position.other], 1998, 2021, 'sfdg')

    holder.add_genre(Genre.action)
    holder.add_genre(Genre.horror)
    holder.add_genre(Genre.melodrama)

    holder.add_user_type(UserType.plain_user)
    holder.add_user_type(UserType.admin)

    holder.add_user(User(20, UserType.plain_user, '07.07.2021 1:00','07.07.2021 1:11'))
    holder.add_user(User(10, UserType.plain_user, '06.07.2021 14:00','07.07.2021 16:16'))
    a = Params(2000, 2020, [Genre.action, Genre.melodrama], 1, 3, True, False, 20)
    b = Params(1990, 2015, [Genre.horror, Genre.melodrama], 2, 5, False, False, 10)
    holder.add_params(a)
    holder.add_params(b)
    holder.add_req(Req(20, a))
    holder.add_req(Req(10, b))
    holder.add_fav(Req(20, a))
    holder.add_fav(Req(10, b))
    holder.remove_fav(Req(20, a))

    holder.add_person(Person(700, 'SAM', Position.actor, 1990, 2021, 'dafsgdfhasd'))
    holder.add_person(Person(450, 'BEN', Position.actor, 1985, 2019, '1234567wsadf'))
    holder.add_relation(Relation(700, 450, 7, b), b)

    DBWork.show_all_tables_values()
    print(holder.has_params(b))
    print(holder.is_part(Params(1990, 2015, [Genre.horror, Genre.melodrama], 1, 5, False, False, 10)))
    print(holder.get_full(b))

if __name__ == '__main__':
    print_hi('PyCharm')
