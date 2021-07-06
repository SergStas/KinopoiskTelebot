import db.DBWork

class DBHolder:  # TODO:  Stepa
    @staticmethod
    def add_genre(genreIN):
        if (db.DBWork.execute_query_to_return(
                "select * from genre where id = {0} and name = '{1}'".format(genreIN.value, genreIN.name)) == []):
            db.DBWork.execute_query(
                "insert into genre (id, name) values ({0},'{1}')".format(genreIN.value, genreIN.name))


    @staticmethod
    def get_genres():
        return [] # ВОПРОС ЗАЧЕМ, есть енум


    @staticmethod
    def add_person(personIN):  # person_id, full_name, photo_url
        if (db.DBWork.execute_query_to_return("select * from person where {0} = id".format(personIN.person_id)) == []):
            db.DBWork.execute_query("insert into person (id, full_name, photo_url) "
                                    "values ({0},'{1}',{2})".format(personIN.person_id, personIN.full_name,
                                                                         personIN.photo_url))


    @staticmethod
    def add_params(params): #id, person_id, start_year, end_year, threshold, is_actor
        if(db.DBWork.execute_query_to_return("select * from params where id = {0}".format(params.id)) == []):
            db.DBWork.execute_query("insert into params (id, person_id, start_year, end_year, threshold, is_actor) "
                            "values ({0}, {1}, {2}, {3}, {4}, {5})"
                            .format(params.id, params.person_id, params.start_year, params.end_year, params.threshold, params.is_actor))


    @staticmethod
    def add_relation(relation, params): # RELATION: person_id1, person_id2, count_films PARAMS: id
        if(db.DBWork.execute_query_to_return("select * from colleague where person_id1 = {0} and person_id2 = {1} and params_id = {2}"
                                             .format(relation.first, relation.second, params.id)) == []):
            db.DBWork.execute_query("insert into colleague (person_id1, person_id2, params_id, count_films) values "
                                    "({0}, {1}, {2}, {3})".format(relation.first, relation.second, relation.weight, params.id))



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
    def add_user_type(user_type):
        pass


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

