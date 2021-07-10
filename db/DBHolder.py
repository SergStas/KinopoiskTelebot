import sys
import db.DBWork
from models.dataclasses.Params import Params
from models.dataclasses.Person import Person
from models.dataclasses.Relation import Relation
from models.dataclasses.Req import Req


class DBHolder:
    @staticmethod
    def get_genres():
        result = [row[0] for row in db.DBWork.execute_query_to_return('select name from genre')]
        return result

    @staticmethod
    def get_genres_with_ids():
        result = [(row[0], row[1]) for row in db.DBWork.execute_query_to_return('select id, name from genre')]
        return result

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
        str_start = params.start_year if params.start_year is not None else -1
        str_end = params.end_year if params.end_year is not None else -1
        str_act = params.actors_only if params.actors_only is not None else 'null'
        par = DBHolder.__get_params(params, False)
        print('pars:')
        print(par)
        # genres = params.genres if len(params.genres) > 0 else [e[0] for e in
        #                                                        db.DBWork.execute_query_to_return('select * from genre')]
        all_same = True
        if par:
            for p in par:
                all_same = all_same and DBHolder.equals_genres_list(p[0], params.genres)
                print(all_same)
        if par == [] or not all_same:
            db.DBWork.execute_query("insert into params (person_id, start_year, end_year, threshold, is_actors, rank) "
                                    "values ({0}, {1}, {2}, {3}, {4}, {5})"
                                    .format(params.person.person_id, str_start, str_end,
                                            params.threshold,
                                            str_act, params.rank))
            params_id = DBHolder.__get_params(params, False)[0][0]
            print('genres:')
            print(params.genres)
            for genre in params.genres:
                g_id = db.DBWork.execute_query_to_return("select id from genre where name = '{0}'".format(genre))
                print(params_id)
                print(g_id[0][0])
                if not g_id:
                    DBHolder.add_genre(genre)
                    g_id = db.DBWork.execute_query_to_return("select id from genre where name = '{0}'".format(genre))
                if not db.DBWork.execute_query_to_return(
                        "select * from params_genre where params_id = {0} and genre_id = {1}".format(params_id,
                                                                                                     g_id[0][0])):
                    db.DBWork.execute_query("insert into params_genre (genre_id, params_id) VALUES ({0},{1})"
                                            .format(g_id[0][0], params_id))

    @staticmethod
    def __get_params(params, except_thr):
        str_start = params.start_year if params.start_year is not None else -1
        str_end = params.end_year if params.end_year is not None else -1
        str_act = params.actors_only if params.actors_only is not None else -1
        thr = f' and threshold = {params.threshold}' if not except_thr else ''
        return db.DBWork.execute_query_to_return(f"select * from params where person_id = {params.person.person_id} "
                                                 f"and start_year = {str_start} and end_year = {str_end}"
                                                 f"{thr} "
                                                 f"and is_actors = {str_act} and rank = {params.rank}")

    @staticmethod
    def equals_genres_list(p_id1, g2):
        genres = db.DBWork.execute_query_to_return(
            "select g.name from params_genre p join genre g on p.genre_id = g.id "
            "where p.params_id = {0}".format(p_id1))
        result = [g[0] for g in genres]
        return set(result) == set(g2)

    @staticmethod
    def add_relation(relation):
        params_id = DBHolder.find_id_in_params(relation.params)
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
        par_exists = DBHolder.__get_params(params, False)
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
        id = DBHolder.find_id_in_params(params)
        rels = db.DBWork.execute_query_to_return("select * from colleague where params_id = {0}".format(id))
        for rel in rels:
            person1 = db.DBWork.person_query("select * from person where id = {0}".format(rel[0]))[0]
            person2 = db.DBWork.person_query("select * from person where id = {0}".format(rel[1]))[0]
            p = db.DBWork.execute_query_to_return("select * from params where id = {0}".format(rel[2]))
            result.append(Relation(person1, person2, rel[3], params))
        return result

    @staticmethod
    def is_part(params):
        result = sys.maxsize
        par = DBHolder.__get_params(params, True)
        if not par:
            return False
        else:
            thr = DBHolder.find_threshold_in_params(params)
            for t in thr:
                if params.threshold > t and (result < t or result == sys.maxsize):
                    result = t
        return result < params.threshold

    @staticmethod
    def get_part(params):  # Relation[]
        thr = DBHolder.find_threshold_in_params(params)[0]
        id = DBHolder.find_id_in_params(params)
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
    def find_id_in_params(params):
        ids = DBHolder.__get_params(params, False)
        # genres = params.genres if len(params.genres) != 0 else [e[0] for e in
        #                                                         db.DBWork.execute_query_to_return(
        #                                                             'select id from genre')]
        print(params.genres)
        print(ids)
        result = None
        for id in ids:
            if DBHolder.equals_genres_list(id[0], params.genres):
                result = id
        return result[0]

    @staticmethod
    def find_threshold_in_params(params):  # int
        pars = DBHolder.__get_params(params, True)
        result = []
        print(pars)
        print(params.genres)
        for par in pars:
            if DBHolder.equals_genres_list(par[0], params.genres):
                result.append(par[4])
        return result

    @staticmethod
    def get_min_threshold(params):  # int
        # поиск точно таких же параметров, но порог которых выше, возвращение наименьшего порога (то есть ближайшего);
        # если параметров таких вообще нет, то возвращает 0
        result = None
        g = params.genres
        params.genres = g if len(g) > 0 else DBHolder.get_genres()
        thr = DBHolder.find_threshold_in_params(params)
        print(thr)
        params.genres = g
        print([e for e in thr if e > params.threshold])
        if len([e for e in thr if e > params.threshold]) == 0:
            return 0
        return max([e for e in thr if e > params.threshold])
        # for m in thr:
        #     if params.threshold < m and (result is None or result > m):
        #         result = m
        # if result is None:
        #     result = 0
        # return result

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
        params_id = DBHolder.find_id_in_params(req.params)
        if (db.DBWork.execute_query_to_return(
                "select * from req where user_id = {0} and params_id = {1} and date = '{2}'"
                        .format(req.user_id, params_id, req.date)) == []):
            db.DBWork.execute_query(
                "insert into req (user_id, params_id, date) values ({0},{1},'{2}')".format(req.user_id, params_id,
                                                                                           req.date))

    @staticmethod
    def show_reqs(user):
        result = [Req(user_id=e[1], date=e[3], params=DBHolder.get_params_by_id(e[2]))
                  for e in db.DBWork.execute_query_to_return(
                f'select * from req where user_id = {user.user_id}'
            )]
        return result
        # return DBHolder.create_params_to_return(
        #     db.DBWork.execute_query_to_return("select * from req where user_id = {0}"
        #                                       .format(user.user_id)))

    @staticmethod
    def add_fav(req):
        params_id = DBHolder.find_id_in_params(req.params)
        if (db.DBWork.execute_query_to_return(
                "select * from req where user_id = {0} and params_id = {1} and date = '{2}'"
                        .format(req.user_id, params_id, req.date)) == []):
            return
        id = DBHolder.find_id_in_req(req.user_id, params_id, req.date)
        if not db.DBWork.execute_query_to_return("select * from fav where req_id = {0}".format(id)):
            db.DBWork.execute_query("insert into fav (req_id) values ({0})".format(id))

    @staticmethod
    def remove_fav(req):
        params_id = DBHolder.find_id_in_params(req.params)
        if (db.DBWork.execute_query_to_return(
                "select * from req where user_id = {0} and params_id = {1} and date = '{2}'"
                        .format(req.user_id, params_id, req.date)) != []):
            id = DBHolder.find_id_in_req(req.user_id, params_id, req.date)
            if (db.DBWork.execute_query_to_return("select * from fav where req_id = {0}".format(id)) != []):
                db.DBWork.execute_query("delete from fav where req_id = {0}".format(id))

    @staticmethod
    def show_favs(user):  #
        result = [Params(DBHolder.get_person_by_id(e[1]), e[2], e[3],
                         DBHolder.get_genres_for_params(e[0]), e[4], e[6], e[5], e[8], e[7])
                  for e in db.DBWork.execute_query_to_return(
                f'select p.* from params p join req r on p.id = r.params_id join fav f on r.id = f.req_id'
                f' where user_id = {user.user_id}'
            )]
        return result
        # all_req = db.DBWork.execute_query_to_return("select * from req where user_id = {0}".format(user.user_id))
        # favs = []
        # for req in all_req:
        #     if (db.DBWork.execute_query_to_return("select * from fav where req_id = {0}".format(req[0])) != []):
        #         favs.append(req)
        # return DBHolder.create_params_to_return(favs)

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

    @staticmethod
    def find_req_by_ids(params, user_id):
        params_id = DBHolder.__get_params(params, False)[0][0]
        return [Req(params=params, user_id=user_id, date=e[3])
                for e in db.DBWork.execute_query_to_return(
                f'select * from req where user_id = {user_id} and params_id = {params_id}')][0]

    @staticmethod
    def get_params_by_id(params_id):
        return [Params(DBHolder.get_person_by_id(e[1]), e[2], e[3],
                       DBHolder.get_genres_for_params(e[0]), e[4], e[6], e[5], e[8], e[7])
                for e in db.DBWork.execute_query_to_return(
                f'select * from params where id = {params_id}'
            )][0]

    @staticmethod
    def get_genres_for_params(params_id):
        return [e[0] for e in db.DBWork.execute_query_to_return(
            f'select name from params_genre p join genre g on p.genre_id = g.id where params_id = {params_id}')]

    @staticmethod
    def get_person_by_id(person_id):
        return [Person(e[0], e[1], e[2]) for e in db.DBWork.execute_query_to_return(
            f'select * from person where id = {person_id}')][0]
