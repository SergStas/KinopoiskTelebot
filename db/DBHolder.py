import db.DBWork
from db import DBWork
from models.dataclasses.Person import Person
from models.enums.Position import Position


class DBHolder:  # TODO:  Stepa
    @staticmethod
    def add_genre(genreIN):
        if (db.DBWork.execute_query_to_return(
                "select * from genre where id = {0} and name = '{1}'".format(genreIN.value, genreIN.name)) == []):
            db.DBWork.execute_query(
                "insert into genre (id, name) values ({0},'{1}')".format(genreIN.value, genreIN.name))


    @staticmethod
    def add_person(personIN):  # person_id, full_name, photo_url
        if (db.DBWork.execute_query_to_return("select * from person where {0} = id".format(personIN.person_id)) == []):
            db.DBWork.execute_query("insert into person (id, full_name, ) "
                                    "values ({0},'{1}',{2}, {3})".format(personIN.person_id, personIN.full_name,
                                                                         personIN.start_year, personIN.end_year))


    @staticmethod
    def add_params(param):
        pass


    @staticmethod
    def add_relation(relation, params):
        pass


    @staticmethod
    def get_genres():
        return []


    @staticmethod
    def has_params(params): # boolean
        pass


    @staticmethod
    def get_full(params): # Relation[]
        return []


    @staticmethod
    def is_part(params): # boolean // все то же самое, кроме порога: существующий порог ниже требуемого
        pass


    @staticmethod
    def get_part(params): # Relation[] // сохранение новых параметров, сохранение связей с новыми параметрами
        return []


    @staticmethod
    def get_min_threshold(params): #int
        # поиск точно таких же параметров, но порог которых выше, возвращение наименьшего порога (то есть ближайшего);
        # если параметров таких вообще нет, то возвращает 0
        pass


    @staticmethod
    def add_user(user): #start_date_use add
        pass


    @staticmethod
    def add_req():
        pass
