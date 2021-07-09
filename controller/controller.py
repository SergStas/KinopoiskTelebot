from db.DBHolder import DBHolder
from graph.GraphGenerator import GraphGenerator
from network.NetworkModule import NetworkModule


class KinopoiskBotController:
    @staticmethod
    def get_persons_list(full_name):
        return NetworkModule.get_actors(full_name)

    @staticmethod
    def get_graph(params, progress_bar):
        if (params.generate_gif is None) | (params.generate_gif == False):
            return KinopoiskBotController._process_single_graph(params, progress_bar)

    @staticmethod
    def _process_single_graph(params, progress_bar):
        relations = KinopoiskBotController._get_relations(params, progress_bar)
        return GraphGenerator.get_graph(params, relations)

    @staticmethod
    def _get_relations(params, progress_bar):
        if DBHolder.has_params(params):
            return DBHolder.get_full(params)
        if DBHolder.is_part(params):
            return DBHolder.get_part(params)
        existing_threshold = DBHolder.get_min_threshold(params)
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
