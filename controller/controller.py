import datetime

from db import DBWork
from db.DBHolder import DBHolder
from graph.GraphGenerator import Graph, Gif, Chart
from models.dataclasses.Req import Req
from network.NetworkModule import NetworkModule


class KinopoiskBotController:
    @staticmethod
    def get_visits():
        visit_stats = DBHolder.get_visit_stats()
        return Chart.get_visits_chart(visit_stats)

    @staticmethod
    def init():
        DBWork.start_bd()

    @staticmethod
    def get_graph(params, progress_bar, user_id):
        if (params.generate_gif is None) or (not params.generate_gif):
            return KinopoiskBotController._process_single_graph(params, progress_bar, user_id)
        return Gif(params).get_gif()

    @staticmethod
    def get_persons_list(full_name):
        return NetworkModule.get_actors(full_name)

    @staticmethod
    def add_fav(params, user_id):
        req = DBHolder.find_req_by_ids(params, user_id)
        DBHolder.add_fav(req)

    @staticmethod
    def remove_fav(params, user_id):
        DBHolder.remove_fav(DBHolder.find_req_by_ids(params, user_id))

    @staticmethod
    def get_favorites(user):
        return DBHolder.show_favs(user)

    @staticmethod
    def add_user(user):
        DBHolder.add_user(user)

    @staticmethod
    def add_req(params, user_id):
        DBHolder.add_req(Req(params=params, user_id=user_id, date=datetime.date.today()))

    @staticmethod
    def get_history(user):
        return DBHolder.show_reqs(user)

    @staticmethod
    def _process_single_graph(params, progress_bar, user_id):
        relations = KinopoiskBotController._get_relations(params, progress_bar)
        print('relations got')
        g = params.genres
        params.genres = params.genres if len(params.genres) > 0 else DBHolder.get_genres()
        KinopoiskBotController.add_req(params, user_id)
        params.genres = g
        return Graph(relations=relations, params=params).draw_graph()

    @staticmethod
    def _get_relations(params, progress_bar):
        DBHolder.add_person(params.person)
        if DBHolder.has_params(params):
            print('params found')
            g = params.genres
            params.genres = params.genres if len(params.genres) > 0 else DBHolder.get_genres()
            result = DBHolder.get_full(params)
            params.genres = g
            return result
        if DBHolder.is_part(params):
            print('subgraph found')
            rels = DBHolder.get_part(params)
            g = params.genres
            params.genres = params.genres if len(params.genres) > 0 else DBHolder.get_genres()
            DBHolder.add_params(params)
            for rel in rels:
                DBHolder.add_person(rel.second)
                DBHolder.add_relation(rel)
            params.genres = g
            return rels
        existing_threshold = DBHolder.get_min_threshold(params)
        print('request to net...')
        if existing_threshold != 0:
            print('post-loading starts...')
            old = params.threshold
            params.threshold = existing_threshold
            g = params.genres
            params.genres = g if len(params.genres) > 0 else DBHolder.get_genres()
            db_part = DBHolder.get_full(params)
            params.threshold = old
            params.genres = g
            post_loaded_part = \
                KinopoiskBotController._get_relations_from_net(params, progress_bar, existing_threshold)
            g = params.genres
            params.genres = g if len(params.genres) > 0 else DBHolder.get_genres()
            DBHolder.add_params(params)
            for rel in post_loaded_part:
                DBHolder.add_person(rel.second)
                DBHolder.add_relation(rel)
            params.genres = g
            return db_part + post_loaded_part
        g = params.genres
        params.genres = g if len(params.genres) > 0 else DBHolder.get_genres()
        DBHolder.add_params(params)
        params.genres = g
        rels = KinopoiskBotController._get_relations_from_net(params, progress_bar, existing_threshold)
        params.genres = g if len(params.genres) > 0 else DBHolder.get_genres()
        for rel in rels:
            DBHolder.add_person(rel.second)
            DBHolder.add_relation(rel)
        params.genres = g
        return rels

    @staticmethod
    def _get_relations_from_net(params, progress_bar, upper):
        return NetworkModule.get_part(upper, params)
