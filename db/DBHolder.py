import sys
import db.DBWork
from models.dataclasses.Params import Params
from models.dataclasses.Relation import Relation
from models.enums.Genre import Genre


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
            db.DBWork.execute_query("insert into person (id, full_name, photo_url) "
                                    "values ({0},'{1}','{2}')".format(personIN.person_id, personIN.full_name,
                                                                      personIN.url))


    @staticmethod
    def add_params(params):  # person_id, start_year, end_year, threshold, is_actor (Genre[]), rank
        par = db.DBWork.execute_query_to_return("select * from params where person_id = {0} "
                                          "and start_year = {1} and end_year = {2} and threshold = {3} "
                                          "and is_actors = {4} and rank = {5}"
                                          .format(params.person.person_id, params.start_year, params.end_year,
                                                  params.threshold, params.actors_only, params.rank))
        not_exists = True
        if(par != []):
            for p in par:
                not_exists = not_exists and DBHolder.not_equals_ganres_list(p[0], params.genres)
        if (par == [] or not_exists):
            db.DBWork.execute_query("insert into params (person_id, start_year, end_year, threshold, is_actors, rank) "
                                    "values ({0}, {1}, {2}, {3}, {4}, {5})"
                                    .format(params.person.person_id, params.start_year, params.end_year, params.threshold,
                                            params.actors_only, params.rank))
            id = db.DBWork.execute_query_to_return("select id from params where person_id = {0} and start_year = {1} "
                                                 "and end_year = {2} and threshold = {3} and is_actors = {4} and rank = {5}"
                                                 .format(params.person.person_id, params.start_year, params.end_year,
                                                         params.threshold, params.actors_only, params.rank))[0][0]
            for genre in params.genres:
                g_id = db.DBWork.execute_query_to_return("select id from genre where name = {0}".format(genre))
                if(db.DBWork.execute_query_to_return("select * from params_genre where params_id = {0} and genre_id = {1}"
                 .format(id, g_id)) == []):
                    db.DBWork.execute_query("insert into params_genre (genre_id, params_id) VALUES ({0},{1})"
                        .format(g_id, id))

    @staticmethod
    def not_equals_ganres_list(p_id1, g2):
        genres = db.DBWork.execute_query_to_return("select g.name from params_genre p inner join genre g on p.genre_id = g.id "
            "where p.params_id = {0}".format(p_id1))
        list = []
        for g in genres:
            list.append(g[0])
        return set(list) != set(g2) #todo как возвращается genres


    @staticmethod
    def add_relation(relation):  # RELATION: person1, person2, count_films
        params_id = DBHolder.find_id_in_params(relation.params.person.person_id, relation.params.start_year, relation.params.end_year,
                                               relation.params.threshold, relation.params.actors_only, relation.params.rank, relation.params.genres)
        if (db.DBWork.execute_query_to_return(
                "select * from colleague where person_id1 = {0} and person_id2 = {1} and params_id = {2}"
                        .format(relation.first.person_id, relation.second.person_id, params_id)) == []):
            if(db.DBWork.execute_query_to_return("select * from person where id = {0}".format(relation.first.person_id)) != []
            and db.DBWork.execute_query_to_return("select * from person where id = {0}".format(relation.second.person_id)) != []):
                db.DBWork.execute_query("insert into colleague (person_id1, person_id2, params_id, count_films) values "
                                    "({0}, {1}, {2}, {3})".format(relation.first.person_id, relation.second.person_id,
                                                                  params_id, relation.weight))

    @staticmethod
    def has_params(params):  # boolean
        par_exists =  db.DBWork.execute_query_to_return("select * from params where person_id = {0} and start_year = {1} "
                                                 "and end_year = {2} and threshold = {3} and is_actors = {4} and rank = {5}"
                                                 .format(params.person.person_id, params.start_year, params.end_year,
                                                       params.threshold, params.actors_only, params.rank))
        if(par_exists == []):
            return False
        else:
            for p in par_exists:
                if(not DBHolder.not_equals_ganres_list(p[0], params.genres)):
                    return True

    @staticmethod
    def get_full(params):  # Relation[]
        result = []
        id = DBHolder.find_id_in_params(params.person_id, params.start_year, params.end_year, params.threshold,
                                        params.actors_only, params.rank, params.genres)
        rels = db.DBWork.execute_query_to_return("select * from colleague where params_id = {0}".format(id))
        for rel in rels:
            person1 = db.DBWork.person_querry("select * from person where id = {0}".format(rel[0]))
            person2 = db.DBWork.person_querry("select * from person where id = {0}".format(rel[1]))
            p = db.DBWork.execute_query_to_return("select * from params where id = {0}".format(rel[2]))
            result.append(Relation(person1, person2, rel[3], params))
        return result

    @staticmethod
    def is_part(params):  # boolean // все то же самое, кроме порога: существующий порог ниже требуемого
        result = sys.maxsize
        par = db.DBWork.execute_query_to_return("select * from params where person_id = {0} and start_year = {1} "
                                              "and end_year = {2} and is_actors = {3} and rank = {4}"
                                                      .format(params.person.person_id, params.start_year, params.end_year,
                                                              params.actors_only, params.rank))
        if(par == []):
            return False
        else:
            thr = DBHolder.find_threshold_in_params(params.person.person_id, params.start_year, params.end_year,
                                                    params.actors_only, params.rank, params.genres)
            if (type(thr) is type([])):
                for t in thr:
                    if (params.threshold > t[0] and (result < t[0] or result == sys.maxsize)):
                        result = t[0]
        return result < params.threshold

    @staticmethod
    def get_part(params):  # Relation[]
        thr = DBHolder.find_threshold_in_params(params.person.person_id, params.start_year, params.end_year, params.actors_only,
                                                params.rank, params.genres)
        id = DBHolder.find_id_in_params(params.person.person_id, params.start_year, params.end_year, thr, params.actors_only,
                                        params.rank, params.genres)
        answer = db.DBWork.execute_query_to_return("select * from colleague where params_id = {0}".format(id))
        result = []
        for r in answer:
            if (r.weight >= params.threshold):
                person1 = db.DBWork.person_querry("select * from person hwere id = {0}".format(r[0]))
                person2 = db.DBWork.person_querry("select * from person hwere id = {0}".format(r[1]))
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
            if(not DBHolder.not_equals_ganres_list(id[0], genres)):
                result = id
        return result

    @staticmethod
    def find_threshold_in_params(person_id, start_year, end_year, is_actors, rank, genres):  # int
        pars = db.DBWork.execute_query_to_return("select * from params where person_id = {0} and start_year = {1} "
                                                 "and end_year = {2} and is_actors = {3} and rank = {4}"
                                                 .format(person_id, start_year, end_year, is_actors, rank))
        result = []
        for par in pars:
            if(not DBHolder.not_equals_ganres_list(par[0], genres)):
                result.append(par[4])
        return result

    @staticmethod
    def get_min_threshold(params):  # int
        # поиск точно таких же параметров, но порог которых выше, возвращение наименьшего порога (то есть ближайшего);
        # если параметров таких вообще нет, то возвращает 0
        result = None
        thr = DBHolder.find_threshold_in_params(params.person.person_id, params.start_year, params.end_year, params.actors_only,
                                                params.rank, params.genres)
        if(type(thr) is type([])):
            for t in thr:
                for m in t:
                    if(params.threshold < m and (result is None or result > m )):
                        result = m
        else:
            result = thr
        if result is None:
            result = 0
        return result

    @staticmethod
    def add_user_type(user_type):
        if (db.DBWork.execute_query_to_return("select * from user_type where id = {0} and name = '{1}'"
                                                      .format(user_type.value, user_type.name)) == []):
            db.DBWork.execute_query(
                "insert into user_type (id, name) values ({0}, '{1}')".format(user_type.value, user_type.name))


    @staticmethod
    def add_user(user):  # id, start_date_use, date_last_visit, user_type_id
        if (db.DBWork.execute_query_to_return("select * from user where id = {0}".format(user.user_id)) == []):
            db.DBWork.execute_query("insert into user (id, name, start_date_active, last_date_active, user_type_id) values "
                                    "({0},'{1}','{2}','{3}', {4})".format(user.user_id, user.name, user.start_date_active,
                                                                   user.last_date_active, user.user_type))

    @staticmethod
    def update_user(user):
        if (db.DBWork.execute_query_to_return("select * from user where id = {0}".format(user.user_id)) != []):
            db.DBWork.execute_query(
                "update user set last_date_active = '{0}', user_type_id = {1} where id = {2}"
                    .format(user.last_date_active, user.user_type, user.user_id))

    @staticmethod
    def get_users(): #
        return db.DBWork.user_querry("select * from user")

    @staticmethod
    def add_req(req):  # user_id, params
        params_id = DBHolder.find_id_in_params(req.params.person.person_id, req.params.start_year, req.params.end_year,
                                               req.params.threshold, req.params.actors_only, req.params.rank, req.params.genres)
        if (db.DBWork.execute_query_to_return("select * from req where user_id = {0} and params_id = {1} and date = '{2}'"
                                      .format(req.user_id, params_id, req.date)) == []):
            db.DBWork.execute_query(
                "insert into req (user_id, params_id, date) values ({0},{1},'{2}')".format(req.user_id, params_id, req.date))

    @staticmethod
    def show_reqs(user): #
        return DBHolder.create_params_to_return(db.DBWork.execute_query_to_return("select * from req where user_id = {0}"
                                                                                  .format(user.user_id)))

    @staticmethod
    def add_fav(req):  # user_id, params, date
        params_id = DBHolder.find_id_in_params(req.params.person.person_id, req.params.start_year, req.params.end_year,
                                               req.params.threshold, req.params.actors_only, req.params.rank, req.params.genres)
        if (db.DBWork.execute_query_to_return("select * from req where user_id = {0} and params_id = {1} and date = '{2}'"
                                     .format(req.user_id, params_id, req.date)) != []):
            id = DBHolder.find_id_in_req(req.user_id, params_id, req.date)
            if(db.DBWork.execute_query_to_return("select * from fav where req_id = {0}".format(id)) == []):
                db.DBWork.execute_query("insert into fav (req_id) values ({0})".format(id))

    @staticmethod
    def remove_fav(req):
        params_id = DBHolder.find_id_in_params(req.params.person.person_id, req.params.start_year, req.params.end_year,
                                               req.params.threshold, req.params.actors_only, req.params.rank, req.params.genres)
        if (db.DBWork.execute_query_to_return("select * from req where user_id = {0} and params_id = {1} and date = '{2}'"
                                                      .format(req.user_id, params_id,req.date)) != []):
            id = DBHolder.find_id_in_req(req.user_id, params_id, req.date)
            if (db.DBWork.execute_query_to_return("select * from fav where req_id = {0}".format(id)) != []):
                db.DBWork.execute_query("delete from fav where req_id = {0}".format(id))

    @staticmethod
    def show_favs(user): #
        all_req = db.DBWork.execute_query_to_return("select * from req where user_id = {0}".format(user.user_id))
        favs = []
        for req in all_req:
            if(db.DBWork.execute_query_to_return("select * from fav where req_id = {0}".format(req[0])) != []):
                favs.append(req)
        return DBHolder.create_params_to_return(favs)

    @staticmethod
    def create_params_to_return(all_req):
        result = []
        params_ex = []
        if (all_req != []):
            for req in all_req:
                params_ex.append(db.DBWork.execute_query_to_return("select * from req r inner join params p "
                                                                   "on r.params_id = p.id where r.id = {0}".format(
                    req[0])))
        for params_req in params_ex:
            genres = db.DBWork.execute_query_to_return(
                "select genre_id from params_genre where params_id = {0}".format(params_req[4]))
            genres_enum = []
            for g in genres:
                genres_enum.append(Genre(g))
            result.append(
                Params(params_req[5], params_req[6], params_req[7], genres_enum, params_req[8], params_req[10],
                       params_req[9], None, None, None))
        return result

    @staticmethod
    def find_id_in_req(user_id, params_id, date):
        answer = db.DBWork.execute_query_to_return("select id from req  where user_id = {0} and params_id = {1} and date ='{2}'"
                                                 .format(user_id, params_id, date))
        if(answer != []):
            answer = answer[0][0]
        return answer