import time

import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont  # Это нужно для того, чтобы создавать пустые картинки
import imageio
from threading import current_thread

from models.dataclasses.GraphData import GraphData
from models.dataclasses.Params import Params
from network.NetworkModule import NetworkModule


class Graph:
    _path = 'img/'

    def __init__(self, relations, params):
        self.params = params
        self.relations = [[rel.first.full_name, rel.second.full_name, rel.weight] for rel in relations]
        print(self.relations)
        self.father = params.person.full_name
        # Тот с чего все началось, его вершина будет окрашена красным, скорее всего будет приходить с
        # запросом, следовательно дополнить __init_ еще на один аргумент
        self.w = 20  # Для графика высота по пикселям
        self.h = 20  # для графика гирина по пикселям
        self.d = 100  # Для  графика, не помню зачем нужна, но нужна!
        self.G = nx.Graph()

    def draw_graph(self):
        self.G.add_weighted_edges_from(self.relations)  # Все, G у нас набит связями
        plt.figure(figsize=(self.w, self.h), dpi=self.d)
        # print(self.G.edges())
        color_map = {self.father: 'pink'}  # Создадим Словаь цветов вершин, которые мы хотим покрасить
        values = [color_map.get(node, "Teal") for node in self.G.nodes()]# cоздаем словарь цветов для всех,
        edge_labels = dict([((u, v,), d['weight'])
                            for u, v, d in self.G.edges(data=True)])

        posi = nx.spring_layout(self.G)
        nx.draw(self.G, pos=posi, node_color=values, node_size=1500,
                with_labels=True)  # цшер_дфиуды - отображать название, еще сюда из интересного можно вставить
        # edge_color=["r","b"] например,, это окрасит ребра
        nx.draw_networkx_edge_labels(self.G, posi, edge_labels=edge_labels)

        path = f'{Graph._path}graph{current_thread().name}.png'
        plt.savefig(path)  # График оборачивается в картинку
        return GraphData(path, self.params)

    # def frame_shot(self):  # Нарезка кадров от начала создания графа до создания последней вершины
    #     new = []  # Здесь будут храниться self.relations, постепенно заполняемые значениями
    #     images = []  # Здесь будут храниться наши снимки
    #     ps = nx.spring_layout(self.G)

    #     position_new = {}
    #     path = None
    #     for element in self.relations:

    #         for x in ps.keys():
    #             if position_new != {}:
    #                 for y in position_new.keys():
    #                     condition = False
    #                     if y == x:
    #                         condition = True
    #                         break
    #                 if not condition:
    #                     position_new[x] = ps[x]
    #             else:
    #                 position_new[x] = ps[x]

    #         new.append(element)
    #         H = nx.Graph()
    #         plt.figure(figsize=(self.w, self.h), dpi=self.d)
    #         H.add_weighted_edges_from(new)  # По вершинам
    #         nx.draw(H, pos=position_new, node_size=700, with_labels=True)
    #         nx.draw_networkx_edge_labels(H, position_new)
    #         path = f'{Graph._path}buf{current_thread().name}.png'
    #         plt.savefig(path)
    #         images.append(imageio.imread(path))

    #     kargs = {'duration': 0.5}
    #     imageio.mimsave(f'{Graph._path}movie{current_thread().name}.gif', images, **kargs)
    #     print('done')
    #     return GraphData(path=path, params=self.params)


class gif:
    _path = "gif/"
    def __init__(self, params):
        self.params = params
        self.images = []


    def make_response(self, start_year, end_year):
        params = Params(start_year=start_year, end_year=end_year, person=self.params.person,
                        threshold=self.params.threshold, genres=self.params.genres, rank=self.params.rank,
                        actors_only=self.params.actors_only, generate_gif=self.params.generate_gif,
                        name=self.params.name, step=self.params.step)
        relations = NetworkModule.get_relations(params)
        return (relations, params)

    def get_gif(self):
        for i in range(self.params.start_year, self.params.end_year, self.params.step):
            rels = self.make_response(i, i + self.params.step)
            self.__append(rels[0], rels[1])
        path = self.merge()
        return GraphData(path=path, params=self.params)
        
    @staticmethod
    def __create_graph(relations, params):
        graph = Graph(relations, params)
        x = graph.draw_graph()
        path = x.path
        return path
    
    def __append(self, relations, params, name = 'movie'):
        path = self.__create_graph(relations, params)
        print(f'appended frame with {len(relations)} edges')
        self.images.append(imageio.imread(path))
        
    def merge(self):
        kargs = { 'duration': 0.5 }
        imageio.mimsave(f'{self._path}movie{current_thread().name}.gif', self.images, **kargs)
        return f'{self._path}movie{current_thread().name}.gif'
