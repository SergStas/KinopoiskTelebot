from db import DBWork
from db.DBHolder import DBHolder
from graph.GraphGenerator import Graph
from models.dataclasses.Params import Params
from network.NetworkModule import NetworkModule, RequestManager
from network.SeleniumSessionHandler import SeleniumSessionHandler


class KinopoiskBotController:
    @staticmethod
    def init():
        DBWork.start_bd()
        RequestManager.init_session()

    @staticmethod
    def get_graph(params, progress_bar):
        try:
            i = params.person.person_id
        except:
            params.person = NetworkModule.get_person_by_id(params.person_id)
        if (params.generate_gif is None) | (not params.generate_gif):
            return KinopoiskBotController._process_single_graph(params, progress_bar)

    @staticmethod
    def get_persons_list(full_name):
        return NetworkModule.get_actors(full_name)

    @staticmethod
    def add_fav(params):
        DBHolder.add_fav(params)

    @staticmethod
    def remove_fav(params):
        DBHolder.remove_fav(params)

    @staticmethod
    def get_favorites(user):
        return DBHolder.show_favs(user)

    @staticmethod
    def add_user(user):
        DBHolder.add_user(user)

    @staticmethod
    def get_history(user):
        return DBHolder.show_reqs(user)

    @staticmethod
    def _process_single_graph(params, progress_bar):
        relations = KinopoiskBotController._get_relations(params, progress_bar)
        print('relations got')
        return Graph(relations=relations, params=params).draw_graph()

    @staticmethod
    def _get_relations(params, progress_bar):
        if DBHolder.has_params(params):
            print('params found')
            return DBHolder.get_full(params)
        if DBHolder.is_part(params):
            print('subgraph found')
            return DBHolder.get_part(params)
        existing_threshold = DBHolder.get_min_threshold(params)
        print('request to net...')
        if existing_threshold != 0:
            old = params.threshold
            params.threshold = existing_threshold
            db_part = DBHolder.get_full(params)
            params.threshold = old
            post_loaded_part = \
                KinopoiskBotController._get_relations_from_net(params, progress_bar, existing_threshold)
            return db_part + post_loaded_part
        return KinopoiskBotController._get_relations_from_net(params, progress_bar, existing_threshold)

    @staticmethod
    def _get_relations_from_net(params, progress_bar, upper):
        return NetworkModule.get_part(upper, params)
