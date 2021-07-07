import sys

import db.DBWork


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
                                                                      personIN.photo_url))

    @staticmethod
    def add_params(params):  # person_id, start_year, end_year, threshold, is_actor (Genre[])
        if (db.DBWork.execute_query_to_return("select * from params where person_id = {0} "
                                              "and start_year = {1} and end_year = {2} and threshold = {3} and is_actors = {4}"
                                                      .format(params.person_id, params.start_year, params.end_year,
                                                              params.threshold, params.is_actors)) == []):
            db.DBWork.execute_query("insert into params (person_id, start_year, end_year, threshold, is_actors) "
                                    "values ({0}, {1}, {2}, {3}, {4})"
                                    .format(params.person_id, params.start_year, params.end_year, params.threshold,
                                            params.is_actors))
            id = DBHolder.find_id_in_params(params.person_id, params.start_year, params.end_year, params.threshold,
                                            params.is_actors)
            for genre in params.genres_to_remove:
                if(db.DBWork.execute_query_to_return("select * from params_genre where params_id = {0} and genre_id = {1}"
                 .format(id, genre.value)) == []):
                    db.DBWork.execute_query("insert into params_genre (genre_id, params_id) VALUES ({0},{1})".format(genre.value, id))

    @staticmethod
    def add_relation(relation, params):  # RELATION: person_id1, person_id2, count_films PARAMS: id
        params_id = DBHolder.find_id_in_params(params.person_id, params.start_year, params.end_year, params.threshold,
                                        params.is_actors)
        if (db.DBWork.execute_query_to_return(
                "select * from colleague where person_id1 = {0} and person_id2 = {1} and params_id = {2}"
                        .format(relation.first, relation.second, params_id)) == []):
            if(db.DBWork.execute_query_to_return("select * from person where id = {0}".format(relation.first)) != []
            and db.DBWork.execute_query_to_return("select * from person where id = {0}".format(relation.second)) != []):
                db.DBWork.execute_query("insert into colleague (person_id1, person_id2, params_id, count_films) values "
                                    "({0}, {1}, {2}, {3})".format(relation.first, relation.second, params_id, relation.weight))

    @staticmethod
    def has_params(params):  # boolean
        return db.DBWork.execute_query_to_return("select * from params where person_id = {0} and start_year = {1} "
                                                 "and end_year = {2} and threshold = {3} and is_actors = {4}"
                                                 .format(params.person_id, params.start_year, params.end_year,
                                                         params.threshold, params.is_actors)) != []

    @staticmethod
    def get_full(params):  # Relation[]
        id = DBHolder.find_id_in_params(params.person_id, params.start_year, params.end_year, params.threshold,
                                        params.is_actors)
        return db.DBWork.relation_querry("select * from colleague where params_id = {0}".format(id))

    @staticmethod
    def is_part(params):  # boolean // все то же самое, кроме порога: существующий порог ниже требуемого
        #thr = sys.maxsize
        result = sys.maxsize
        if (db.DBWork.execute_query_to_return("select * from params where person_id = {0} and start_year = {1} "
                                              "and end_year = {2} and is_actors = {3}"
                                                      .format(params.person_id, params.start_year, params.end_year,
                                                              params.is_actors)) != []):
            thr = DBHolder.find_theshold_in_params(params.person_id, params.start_year, params.end_year,
                                                   params.is_actors)
            if (type(thr) is type([])):
                for t in thr:
                    for m in t:
                        if (params.threshold > m and (result < m or result == sys.maxsize)):
                            result = m
        return result < params.threshold

    @staticmethod
    def get_part(params):  # Relation[] // сохранение новых параметров, сохранение связей с новыми параметрами
        thr = DBHolder.find_theshold_in_params(params.person_id, params.start_year, params.end_year, params.is_actors)
        id = DBHolder.find_id_in_params(params.person_id, params.start_year, params.end_year, thr[0][0], params.is_actors)
        answer = db.DBWork.relation_querry("select * from colleague where params_id = {0}".format(id))
        result = []
        for r in answer:
            if (r.weight > params.threshold):
                result.append(r)
        return result # какие новые параметры сохранять?

    @staticmethod
    def find_id_in_params(person_id, start_year, end_year, threshold, is_actors):
        answer = db.DBWork.execute_query_to_return("select id from params where person_id = {0} and start_year = {1} "
                                                 "and end_year = {2} and threshold = {3} and is_actors = {4}"
                                                 .format(person_id, start_year, end_year, threshold, is_actors))
        if(answer != []):
            answer = answer[0][0]
        return answer

    @staticmethod
    def find_theshold_in_params(person_id, start_year, end_year, is_actors):  # int
        return db.DBWork.execute_query_to_return("select threshold from params where person_id = {0} and start_year = {1} "
                                                 "and end_year = {2} and is_actors = {3}"
                                                 .format(person_id, start_year, end_year, is_actors))

    @staticmethod
    def get_min_threshold(params):  # int
        # поиск точно таких же параметров, но порог которых выше, возвращение наименьшего порога (то есть ближайшего);
        # если параметров таких вообще нет, то возвращает 0
        result = None
        thr = DBHolder.find_theshold_in_params(params.person_id, params.start_year, params.end_year, params.is_actors)
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
            db.DBWork.execute_query("insert into user (id, start_date_use, date_last_visit, user_type_id) values "
                                    "({0},'{1}','{2}',{3})".format(user.user_id, user.start_date_use,
                                                                   user.date_last_visit, user.user_type.value))

    @staticmethod
    def update_user(user):
        if (db.DBWork.execute_query_to_return("select * from user where id = {0}".format(user.user_id)) != []):
            db.DBWork.execute_query(
                "update user set start_date_use = '{0}', date_last_visit = '{1}', user_type_id = {2} "
                "where id = {3}".format(user.start_date_use, user.date_last_visit, user.user_type, user.user_id))

    @staticmethod
    def add_req(req):  # user_id, params
        params_id = DBHolder.find_id_in_params(req.params.person_id, req.params.start_year, req.params.end_year,
                                               req.params.threshold, req.params.is_actors)
        if (db.DBWork.execute_query_to_return("select * from req where user_id = {0} and params_id = {1}"
                                                      .format(req.user_id, params_id)) == []):
            db.DBWork.execute_query(
                "insert into req (user_id, params_id) values ({0},{1})".format(req.user_id, params_id))

    @staticmethod
    def show_req(user):
        pass

    @staticmethod
    def add_fav(req):  # user_id, params
        params_id = DBHolder.find_id_in_params(req.params.person_id, req.params.start_year, req.params.end_year,
                                               req.params.threshold, req.params.is_actors)
        if (db.DBWork.execute_query_to_return("select * from req where user_id = {0} and params_id = {1}"
                                                      .format(req.user_id, params_id)) != []):
            id = DBHolder.find_id_in_req(req.user_id, params_id)
            if(db.DBWork.execute_query_to_return("select * from fav where req_id = {0}".format(id)) == []):
                db.DBWork.execute_query("insert into fav (req_id) values ({0})".format(id))

    @staticmethod
    def remove_fav(req):
        params_id = DBHolder.find_id_in_params(req.params.person_id, req.params.start_year, req.params.end_year,
                                               req.params.threshold, req.params.is_actors)
        if (db.DBWork.execute_query_to_return("select * from req where user_id = {0} and params_id = {1}"
                                                      .format(req.user_id, params_id)) != []):
            id = DBHolder.find_id_in_req(req.user_id, params_id)
            if (db.DBWork.execute_query_to_return("select * from fav where req_id = {0}"
                                                          .format(id)) != []):
                db.DBWork.execute_query("delete from fav where req_id = {0}".format(id))

    @staticmethod
    def show_fav(user):
        pass

    @staticmethod
    def find_id_in_req(user_id, params_id):
        answer = db.DBWork.execute_query_to_return("select id from req  where user_id = {0} and params_id = {1}"
                                                 .format(user_id, params_id))
        if(answer != []):
            answer = answer[0][0]
        return answer