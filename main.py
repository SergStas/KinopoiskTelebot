import db.DBWork
import db.DBWork as bd
from db import DBWork
from db.DBHolder import DBHolder as holder
from models.dataclasses.Film import Film
from models.dataclasses.Person import Person
from models.enums.Genre import Genre
from models.enums.Position import Position


def print_hi(name):
    print(f'Hi, {name}')
    bd.start_bd()

    a = Person(0, 'Well Smooth', [Position.actor, Position.other], 1980, 2020)
    b = Person(20, 'Samuel Ponk', [Position.actor], 1990, 2021)
    c = Person(4, 'Ben Cam', [Position.other], 2010, 2021)
    d = Person(1, 'Jim Foos', [Position.other, Position.actor], 1990, 2021)
    e = Person(5, 'Cole Berne', [Position.actor], 1986, 2021)
    f = Person(7, 'Monk Zigh', [Position.actor, Position.other], 1998, 2021)

    holder.add_genre(Genre.action)
    holder.add_genre(Genre.horror)
    holder.add_genre(Genre.melodrama)

    DBWork.show_all_tables_values()


if __name__ == '__main__':
    print_hi('PyCharm')
