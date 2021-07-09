import sys
import db.DBWork
from models.dataclasses.Params import Params
from models.dataclasses.Relation import Relation
from models.enums.Genre import Genre


class DBHolder:
    @staticmethod
    def add_genre(genre):
        if not db.DBWork.execute_query_to_return(f"select * from genre where name = '{genre}'"):
            db.DBWork.execute_query("insert into genre (name) values ('{0}')".format(genre))

    @staticmethod
    def add_person(person):
        if not db.DBWork.execute_query_to_return(f"select * from person where {person.person_id} = id"):
            db.DBWork.execute_query(
                f"insert into person (id, full_name, photo_url) values ({person.person_id},'{person.full_name}','{person.url}')")

    @staticmethod
    def add_params(params):
        par = db.DBWork.execute_query_to_return(f"select * from params where person_id = {params.person.person_id} "
                                                f"and start_year = {params.start_year} and end_year = {params.end_year}"
                                                f" and threshold = {params.threshold} "
                                                f"and is_actors = {params.actors_only} and rank = {params.rank}")
        all_same = True
        if par:
            for p in par:
                all_same = all_same and DBHolder.equals_genres_list(p[0], params.genres)
        if par == [] or not all_same:
            db.DBWork.execute_query("insert into params (person_id, start_year, end_year, threshold, is_actors, rank) "
                                    "values ({0}, {1}, {2}, {3}, {4}, {5})"
                                    .format(params.person.person_id, params.start_year, params.end_year,
                                            params.threshold,
                                            params.actors_only, params.rank))
            params_id = \
                db.DBWork.execute_query_to_return("select id from params where person_id = {0} and start_year = {1} "
                                                  "and end_year = {2} and threshold = {3} and is_actors = {4} and "
                                                  "rank = {5}"
                                                  .format(params.person.person_id, params.start_year, params.end_year,
                                                          params.threshold, params.actors_only, params.rank))[0][0]
            for genre in params.genres:
                g_id = db.DBWork.execute_query_to_return("select id from genre where name = '{0}'".format(genre))
                if not g_id:
                    DBHolder.add_genre(genre)
                    g_id = db.DBWork.execute_query_to_return("select id from genre where name = '{0}'".format(genre))
                if not db.DBWork.execute_query_to_return(
                        "select * from params_genre where params_id = {0} and genre_id = {1}".format(params_id,
                                                                                                     g_id[0][0])):
                    db.DBWork.execute_query("insert into params_genre (genre_id, params_id) VALUES ({0},{1})"
                                            .format(g_id[0][0], params_id))

    @staticmethod
    def equals_genres_list(p_id1, g2):
        genres = db.DBWork.execute_query_to_return(
            "select g.name from params_genre p join genre g on p.genre_id = g.id "
            "where p.params_id = {0}".format(p_id1))
        result = [g[0] for g in genres]
        return set(result) == set(g2)

    @staticmethod
    def add_relation(relation):
        params_id = DBHolder.find_id_in_params(relation.params.person.person_id, relation.params.start_year,
                                               relation.params.end_year,
                                               relation.params.threshold, relation.params.actors_only,
                                               relation.params.rank, relation.params.genres)
        if (db.DBWork.execute_query_to_return(
                "select * from colleague where person_id1 = {0} and person_id2 = {1} and params_id = {2}"
                        .format(relation.first.person_id, relation.second.person_id, params_id)) == []):
            if (db.DBWork.execute_query_to_return(
                    "select * from person where id = {0}".format(relation.first.person_id)) != []
                    and db.DBWork.execute_query_to_return(
                        "select * from person where id = {0}".format(relation.second.person_id)) != []):
                db.DBWork.execute_query("insert into colleague (person_id1, person_id2, params_id, count_films) values "
                                        "({0}, {1}, {2}, {3})".format(relation.first.person_id,
                                                                      relation.second.person_id,
                                                                      params_id, relation.weight))

    @staticmethod
    def has_params(params):
        par_exists = db.DBWork.execute_query_to_return(
            "select * from params where person_id = {0} and start_year = {1} "
            "and end_year = {2} and threshold = {3} and is_actors = {4} and rank = {5}"
                .format(params.person.person_id, params.start_year, params.end_year,
                        params.threshold, params.actors_only, params.rank))
        if not par_exists:
            return False
        else:
            for p in par_exists:
                if DBHolder.equals_genres_list(p[0], params.genres):
                    return True
            return False

    @staticmethod
    def get_full(params):  # Relation[]
        result = []
        id = DBHolder.find_id_in_params(params.person_id, params.start_year, params.end_year, params.threshold,
                                        params.actors_only, params.rank, params.genres)
        rels = db.DBWork.execute_query_to_return("select * from colleague where params_id = {0}".format(id))
        for rel in rels:
            person1 = db.DBWork.person_query("select * from person where id = {0}".format(rel[0]))
            person2 = db.DBWork.person_query("select * from person where id = {0}".format(rel[1]))
            p = db.DBWork.execute_query_to_return("select * from params where id = {0}".format(rel[2]))
            result.append(Relation(person1, person2, rel[3], params))
        return result

    @staticmethod
    def is_part(params):
        result = sys.maxsize
        par = db.DBWork.execute_query_to_return("select * from params where person_id = {0} and start_year = {1} "
                                                "and end_year = {2} and is_actors = {3} and rank = {4}"
                                                .format(params.person.person_id, params.start_year, params.end_year,
                                                        params.actors_only, params.rank))
        if not par:
            return False
        else:
            thr = DBHolder.find_threshold_in_params(params.person.person_id, params.start_year, params.end_year,
                                                    params.actors_only, params.rank, params.genres)
            for t in thr:
                if params.threshold > t and (result < t or result == sys.maxsize):
                    result = t
        return result < params.threshold

    @staticmethod
    def get_part(params):  # Relation[]
        thr = DBHolder.find_threshold_in_params(params.person.person_id, params.start_year, params.end_year,
                                                params.actors_only,
                                                params.rank, params.genres)[0]
        id = DBHolder.find_id_in_params(params.person.person_id, params.start_year, params.end_year, thr,
                                        params.actors_only,
                                        params.rank, params.genres)
        answer = db.DBWork.execute_query_to_return("select * from colleague where params_id = {0}".format(id))
        result = []
        for r in answer:
            if r[3] >= params.threshold:
                person1 = db.DBWork.person_query("select * from person where id = {0}".format(r[0]))[0]
                person2 = db.DBWork.person_query("select * from person where id = {0}".format(r[1]))[0]
                DBHolder.add_params(params)
                new_rel = Relation(person1, person2, r[3], params)
                DBHolder.add_relation(new_rel)
                result.append(new_rel)
        return result

    @staticmethod
    def find_id_in_params(person_id, start_year, end_year, threshold, is_actors, rank, genres):
        ids = db.DBWork.execute_query_to_return("select id from params where person_id = {0} and start_year = {1} "
                                                "and end_year = {2} and threshold = {3} and is_actors = {4} and rank = {5}"
                                                .format(person_id, start_year, end_year, threshold, is_actors, rank))
        result = int
        for id in ids:
            if DBHolder.equals_genres_list(id[0], genres):
                result = id
        return result[0]

    @staticmethod
    def find_threshold_in_params(person_id, start_year, end_year, is_actors, rank, genres):  # int
        pars = db.DBWork.execute_query_to_return("select * from params where person_id = {0} and start_year = {1} "
                                                 "and end_year = {2} and is_actors = {3} and rank = {4}"
                                                 .format(person_id, start_year, end_year, is_actors, rank))
        result = []
        for par in pars:
            if DBHolder.equals_genres_list(par[0], genres):
                result.append(par[4])
        return result

    @staticmethod
    def get_min_threshold(params):  # int
        # поиск точно таких же параметров, но порог которых выше, возвращение наименьшего порога (то есть ближайшего);
        # если параметров таких вообще нет, то возвращает 0
        result = None
        thr = DBHolder.find_threshold_in_params(params.person.person_id, params.start_year, params.end_year,
                                                params.actors_only,
                                                params.rank, params.genres)
        for m in thr:
            if params.threshold < m and (result is None or result > m):
                result = m
        if result is None:
            result = 0
        return result

    @staticmethod
    def add_user_type(user_type):
        if (db.DBWork.execute_query_to_return("select * from user_type where name = '{0}'"
                                                      .format(user_type)) == []):
            db.DBWork.execute_query(
                "insert into user_type (name) values ('{0}')".format(user_type))

    @staticmethod
    def add_user(user):
        if not db.DBWork.execute_query_to_return(f"select id from user_type where name = '{user.user_type}'"):
            DBHolder.add_user_type(user.user_type)
        if not db.DBWork.execute_query_to_return("select * from user where id = {0}".format(user.user_id)):
            db.DBWork.execute_query(
                "insert into user (id, name, start_date_active, last_date_active, user_type_id) values "
                "({0},'{1}','{2}','{3}', '{4}')".format(user.user_id, user.name, user.start_date_active,
                                                        user.last_date_active, user.user_type))

    @staticmethod
    def update_user(user):
        if (db.DBWork.execute_query_to_return("select * from user where id = {0}".format(user.user_id)) != []):
            db.DBWork.execute_query(
                "update user set last_date_active = '{0}', user_type_id = {1} where id = {2}"
                    .format(user.last_date_active, user.user_type, user.user_id))

    @staticmethod
    def get_users():  #
        return db.DBWork.user_querry("select * from user")

    @staticmethod
    def add_req(req):  # user_id, params
        params_id = DBHolder.find_id_in_params(req.params.person.person_id, req.params.start_year, req.params.end_year,
                                               req.params.threshold, req.params.actors_only, req.params.rank,
                                               req.params.genres)
        if (db.DBWork.execute_query_to_return(
                "select * from req where user_id = {0} and params_id = {1} and date = '{2}'"
                        .format(req.user_id, params_id, req.date)) == []):
            db.DBWork.execute_query(
                "insert into req (user_id, params_id, date) values ({0},{1},'{2}')".format(req.user_id, params_id,
                                                                                           req.date))

    @staticmethod
    def show_reqs(user):  #
        return DBHolder.create_params_to_return(
            db.DBWork.execute_query_to_return("select * from req where user_id = {0}"
                                              .format(user.user_id)))

    @staticmethod
    def add_fav(req):
        params_id = DBHolder.find_id_in_params(req.params.person.person_id, req.params.start_year, req.params.end_year,
                                               req.params.threshold, req.params.actors_only, req.params.rank,
                                               req.params.genres)
        if (db.DBWork.execute_query_to_return(
                "select * from req where user_id = {0} and params_id = {1} and date = '{2}'"
                        .format(req.user_id, params_id, req.date)) == []):
            return
        id = DBHolder.find_id_in_req(req.user_id, params_id, req.date)
        if not db.DBWork.execute_query_to_return("select * from fav where req_id = {0}".format(id)):
            db.DBWork.execute_query("insert into fav (req_id) values ({0})".format(id))

    @staticmethod
    def remove_fav(req):
        params_id = DBHolder.find_id_in_params(req.params.person.person_id, req.params.start_year, req.params.end_year,
                                               req.params.threshold, req.params.actors_only, req.params.rank,
                                               req.params.genres)
        if (db.DBWork.execute_query_to_return(
                "select * from req where user_id = {0} and params_id = {1} and date = '{2}'"
                        .format(req.user_id, params_id, req.date)) != []):
            id = DBHolder.find_id_in_req(req.user_id, params_id, req.date)
            if (db.DBWork.execute_query_to_return("select * from fav where req_id = {0}".format(id)) != []):
                db.DBWork.execute_query("delete from fav where req_id = {0}".format(id))

    @staticmethod
    def show_favs(user):  #
        all_req = db.DBWork.execute_query_to_return("select * from req where user_id = {0}".format(user.user_id))
        favs = []
        for req in all_req:
            if (db.DBWork.execute_query_to_return("select * from fav where req_id = {0}".format(req[0])) != []):
                favs.append(req)
        return DBHolder.create_params_to_return(favs)

    @staticmethod
    def create_params_to_return(all_req):
        result = []
        params_ex = []
        if all_req:
            for req in all_req:
                params_ex.append(db.DBWork.execute_query_to_return("select * from req r join params p "
                                                                   "on r.params_id = p.id where r.id = {0}".format(
                    req[0]))[0])
        for params_req in params_ex:
            genres = db.DBWork.execute_query_to_return(
                "select genre_id from params_genre where params_id = {0}".format(params_req[4]))
            genres_enum = []
            for g in genres:
                genres_enum.append(g)
            result.append(
                Params(params_req[5], params_req[6], params_req[7], genres_enum, params_req[8], params_req[10],
                       params_req[9], None, None, None))
        return result

    @staticmethod
    def find_id_in_req(user_id, params_id, date):
        answer = db.DBWork.execute_query_to_return(
            "select id from req where user_id = {0} and params_id = {1} and date ='{2}'"
                .format(user_id, params_id, date))
        if answer:
            answer = answer[0][0]
        return answer
