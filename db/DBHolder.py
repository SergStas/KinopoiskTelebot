import db.DBWork
from db import DBWork
from models.dataclasses.Person import Person


class DBHolder:  # TODO:  Stepa
    @staticmethod
    def add_film(filmIN):  # name, staff, year, genres
        if DBWork.execute_query_to_return("select name from film  where  name = '{0}'".format(filmIN.name)) == []:
            db.DBWork.execute_query(
                "insert into film (name, year) values ('{0}', {1})".format(filmIN.name, filmIN.year))

            f_id = DBWork.execute_query_to_return("select id from film  where name = '{0}'".format(filmIN.name))[0][0]
            for genre in filmIN.genres:
                db.DBWork.execute_query(
                    "insert into genre_film (genre_id, film_id) values ({0},{1})".format(genre.value, f_id))

            for per in filmIN.staff:
                db.DBWork.execute_query("insert into person_film (person_id, film_id) values ({0},{1})"
                                        .format(per.person_id, f_id))
            DBHolder.set_colleague(filmIN)

    @staticmethod
    def set_colleague(filmIN):
        for i in range(0, len(filmIN.staff)):
            for j in range(i + 1, len(filmIN.staff)):
                if filmIN.staff[i].person_id != filmIN.staff[j].person_id:
                    exists21 = db.DBWork.execute_query_to_return(
                        "select * from colleague where person_id2 = {0} and person_id1 = {1}"
                            .format(filmIN.staff[i].person_id, filmIN.staff[j].person_id))
                    exists12 = db.DBWork.execute_query_to_return(
                        "select * from colleague where person_id2 = {0} and person_id1 = {1}"
                            .format(filmIN.staff[j].person_id, filmIN.staff[i].person_id))
                    if (exists21 == [] and exists12 == []):
                        db.DBWork.execute_query(
                            "insert into colleague (person_id1, person_id2, count_films) values ({0},{1},{2})"
                                .format(filmIN.staff[i].person_id, filmIN.staff[j].person_id, 1))
                    elif (exists12 != [] and exists21 == []):
                        DBHolder.update_colleague(filmIN.staff[i].person_id, filmIN.staff[j].person_id, exists12)
                    elif (exists21 != [] and exists12 == []):
                        DBHolder.update_colleague(filmIN.staff[i].person_id, filmIN.staff[j].person_id, exists21)

    @staticmethod
    def update_colleague(p1, p2, exists_exampl):
        for exampl in exists_exampl:
            db.DBWork.execute_query("update colleague set count_films = {0} where person_id1 = {1} and person_id2 = {2}"
                                    .format(exampl[2] + 1, p1, p2))

    @staticmethod
    def add_genre(genreIN):
        db.DBWork.execute_query("insert into genre (id, name) values ({0},'{1}')".format(genreIN.value, genreIN.name))

    @staticmethod
    def add_position(pos):
        db.DBWork.execute_query("insert into position (id, name) values ({0},'{1}')".format(pos.value, pos.name))

    @staticmethod
    def add_person(personIN, film_id):  # person_id, full_name, positions[], start_year, end_year
        if (db.DBWork.execute_query_to_return("select * from person where {0} = id".format(personIN.person_id)) == []):
            db.DBWork.execute_query("insert into person (id, full_name, start_year, end_year) "
                                    "values ({0},'{1}',{2}, {3})".format(personIN.person_id, personIN.full_name,
                                                                         personIN.start_year, personIN.end_year))
        for p in personIN.positions:
            db.DBWork.execute_query(
                "insert into person_position_film (person_id, position_id, film_id) values ({0},{1},{2})"
                .format(personIN.person_id, p.value, film_id))

    @staticmethod
    def get_graph(actor, params):
        return []

    @staticmethod
    def get_all_actors():
        result = []
        names = []
        for pers in db.DBWork.execute_query_to_return(
                "select * from person per inner join person_position_film pp on per.id = pp.person_id"
                " inner join position pos on pos.id = pp.position_id where lower(pos.name) = 'actor'"):
            p = Person(pers[0], pers[1], pers[2], pers[3], pers[4])
            if p.full_name not in names:
                result.append(p)
                names.append(p.full_name)
        return result

    @staticmethod
    def get_all_genres():
        result = []
        for g in db.DBWork.execute_query_to_return("select name from genre"):
            result.append(g[0])
        return result
