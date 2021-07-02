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

    #a = Person(0, 'Well Smooth', [Position.actor, Position.producer], 1980, 2020)
    #b = Person(20, 'Samuel Ponk', [Position.actor], 1990, 2021)
    #c = Person(4, 'Ben Cam', [Position.soundman], 2010, 2021)
    #holder.add_genre(Genre.action)
    #holder.add_genre(Genre.horror)
    #holder.add_genre(Genre.melodrama)
    #holder.add_position(Position.actor)
    #holder.add_position(Position.producer)
    #holder.add_position(Position.soundman)

    #holder.add_film(Film("Soul", [a, b, c], 2012, [Genre.horror, Genre.action]))
    #holder.add_film(Film("DOOM", [a, b, c], 2018, [Genre.melodrama]))

    #holder.add_person(a,1)
    #holder.add_person(b,1)
    #holder.add_person(c,1)
    #holder.add_person(a,2)
    #holder.add_person(b,2)
    #holder.add_person(c,2)

    DBWork.show_all_tables_values()
    for p in holder.get_all_actors():
        print(p.full_name)
    for p in holder.get_all_genres():
        print(p)


if __name__ == '__main__':
    print_hi('PyCharm')
