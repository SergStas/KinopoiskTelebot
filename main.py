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

    db.DBWork.delete_all_tables_values()
    holder.add_genre(Genre.action)
    holder.add_genre(Genre.horror)
    holder.add_genre(Genre.melodrama)

    holder.add_user_type(UserType.plain_user)
    holder.add_user_type(UserType.admin)

    holder.add_user(User(20, UserType.plain_user, '07.07.2021 1:00','07.07.2021 1:11'))
    holder.add_user(User(10, UserType.plain_user, '06.07.2021 14:00','07.07.2021 16:16'))



    holder.add_person(Person(700, 'SAM', Position.actor, 1990, 2021, 'dafsgdfhasd'))
    holder.add_person(Person(450, 'BEN', Position.actor, 1985, 2019, '1234567wsadf'))
    holder.add_person(Person(100, 'LLL', Position.actor, 1990, 2021, 'dafsgdfhasd'))
    holder.add_person(Person(345, 'KKK', Position.actor, 1990, 2021, 'dafsgdfhasd'))
    a = Params(1990, 2015, [Genre.action, Genre.melodrama], 1, 3, True, False, 700)
    c = Params(1990, 2015, [Genre.horror, Genre.melodrama], 3, 5, True, False, 100)
    b = Params(1990, 2015, [Genre.action, Genre.melodrama], 1, 3, True, False, 450)
    f = Params(1990, 2015, [Genre.horror, Genre.melodrama], 3, 5, True, False, 350)
    holder.add_params(a)
    holder.add_params(c)
    holder.add_params(b)
    holder.add_params(f)
    holder.add_relation(Relation(700, 450, 7, a), a)
    holder.add_relation(Relation(100, 345, 8, c), c)

    holder.add_req(Req(20, a))
    holder.add_fav(Req(20, a))

    DBWork.show_all_tables_values()
    print(holder.has_params(Params(1990, 2015, [Genre.horror, Genre.melodrama], 2, 5, True, False, 700)))
    print(holder.is_part(Params(1990, 2015, [Genre.horror, Genre.melodrama], 2, 5, True, False, 700)))
    print(holder.get_min_threshold(Params(1990, 2015, [Genre.horror, Genre.melodrama], 2, 5, True, False, 700)))
    for p in holder.get_part(Params(1990, 2015, [Genre.horror, Genre.melodrama], 2, 5, True, False, 700)):
        print(p.first)
        print(p.second)
        print(p.weight)
        print(p.params)


if __name__ == '__main__':
    print_hi('PyCharm')
