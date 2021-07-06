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
    def add_params(params): # person_id, start_year, end_year, threshold, is_actor
        if(db.DBWork.execute_query_to_return("select * from params where id = {0}".format(params.id)) == []):
            db.DBWork.execute_query("insert into params (person_id, start_year, end_year, threshold, is_actor) "
                            "values ({0}, {1}, {2}, {3}, {4})"
                            .format(params.person_id, params.start_year, params.end_year, params.threshold, params.is_actor))


    @staticmethod
    def add_relation(relation, params): # RELATION: person_id1, person_id2, count_films PARAMS: id
        if(db.DBWork.execute_query_to_return("select * from colleague where person_id1 = {0} and person_id2 = {1} and params_id = {2}"
                                             .format(relation.first, relation.second, params.id)) == []):
            db.DBWork.execute_query("insert into colleague (person_id1, person_id2, params_id, count_films) values "
                                    "({0}, {1}, {2}, {3})".format(relation.first, relation.second, relation.weight, params.id))


    @staticmethod
    def has_params(params): # boolean
        return db.DBWork.execute_query_to_return("select * from params where person_id = {0} start_year = {1} "
                                                 "and end_year = {2} and threshold = {3} and is_actor = {4}"
                 .format(params.person_id, params.start_year, params.end_year, params.threshold, params.is_actor)) != []


    @staticmethod
    def get_full(params): # Relation[]
        id = DBHolder.find_id(params.person_id, params.start_year, params.end_year, params.threshold, params.is_actor)
        return db.DBWork.relation_querry("select * from colleague where params_id = {0}".format(id))


    @staticmethod
    def is_part(params): # boolean // все то же самое, кроме порога: существующий порог ниже требуемого
        thr = int
        if(db.DBWork.execute_query_to_return("select * from params where person_id = {0} start_year = {1} "
                                          "and end_year = {2} and is_actor = {3}"
                                  .format(params.person_id, params.start_year, params.end_year, params.is_actor)) != []):
            thr = DBHolder.find_theshold(params.person_id, params.start_year, params.end_year, params.is_actor)
        return thr < params.threshold


    @staticmethod
    def get_part(params): # Relation[] // сохранение новых параметров, сохранение связей с новыми параметрами
        thr = DBHolder.find_theshold(params.person_id, params.start_year, params.end_year, params.is_actor)
        id = DBHolder.find_id(params.person_id, params.start_year, params.end_year, thr, params.is_actor)
        answer = db.DBWork.relation_querry("select * from colleague where params_id = {0}".format(id))
        result = []
        for r in answer:
            if(r.weight >= params.threshold):
                result.append(r)
        return result


    @staticmethod
    def find_id(person_id, start_year, end_year, threshold, is_actor):
        return db.DBWork.execute_query_to_return("select id from params where person_id = {0} start_year = {1} "
                                          "and end_year = {2} and threshold = {3} and is_actor = {4}"
                                  .format(person_id, start_year, end_year, threshold, is_actor))


    @staticmethod
    def find_theshold(person_id, start_year, end_year, is_actor): #int
        return db.DBWork.execute_query_to_return("select threshold from params where person_id = {0} start_year = {1} "
                                        "and end_year = {2} and is_actor = {3}"
                                        .format(person_id, start_year, end_year, is_actor))

    @staticmethod
    def get_min_threshold(params): #int
        # поиск точно таких же параметров, но порог которых выше, возвращение наименьшего порога (то есть ближайшего);
        # если параметров таких вообще нет, то возвращает 0
        result = None
        for t in DBHolder.find_theshold(params.person_id, params.start_year, params.end_year, params.is_actor):
            result = min(t)
        if result is None:
            result = 0
        return result


    @staticmethod
    def add_user_type(user_type):
        if(db.DBWork.execute_query_to_return("select * from user_type where id = {0} and name = '{1}'"
                                                     .format(user_type.name, user_type.name.value)) == {}):
            db.DBWork.execute_query("insert into user_type (id, name) values ({0}, {1})".format(user_type.name, user_type.value))


    @staticmethod
    def add_user(user): #start_date_use  - add
        pass


    @staticmethod
    def add_req(req):
        pass


    @staticmethod
    def add_fav(req):
        pass


    @staticmethod
    def remove_fav(req):
        pass

