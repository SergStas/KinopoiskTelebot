import time

import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont  # Это нужно для того, чтобы создавать пустые картинки
import imageio

from models.dataclasses.GraphData import GraphData


class Graph:
    _path = '../img/'

    @staticmethod
    def _create_image(text="Похоже здесь пусто, дейкстра не справилась"):  # Создаем картинку с text внутри
        caption = text
        x, y = 25, 250  # Расположение надписи
        font = ImageFont.truetype(font='./impact.ttf', size=20)
        img = Image.new('RGB', (450, 450), color=(255, 255, 255, 0))  # создаем новое изображение
        d = ImageDraw.Draw(img)
        shadowColor = (200, 200, 200)
        thickness = 4
        d.text((x - thickness, y - thickness), caption, font=font, fill=shadowColor,
               thick=thickness)  # Тени создаем, в данном случае влево-вниз
        d.text((x + thickness, y - thickness), caption, font=font, fill=shadowColor, thick=thickness)
        d.text((x - thickness, y + thickness), caption, font=font, fill=shadowColor, thick=thickness)
        d.text((x + thickness, y + thickness), caption, font=font, fill=shadowColor, thick=thickness)
        d.text((x, y), caption, spacing=4, fill=(0, 0, 0), font=font)  # Выводим текст теперь, поверх теней
        print()
        img.save(f'{Graph._path}deikstra.png')

    """Требую правок!!!, напрашивается добавить father"""

    def __init__(self, relations, params):
        self.params = params
        self.relations = relations
        self.father = relations[0][
            0]  # Тот с чего все началось, его вершина будет окрашена красным, скорее всего будет приходить с
        # запросом, следовательно дополнить __init_ еще на один аргумент
        self.w = 20  # Для графика высота по пикселям
        self.h = 20  # для графика гирина по пикселям
        self.d = 60  # Для  графика, не помню зачем нужна, но нужна!

        self.G = nx.Graph()

    def draw_graph(self):
        self.G.add_weighted_edges_from(self.relations)  # Все, G у нас набит связями
        plt.figure(figsize=(self.w, self.h), dpi=self.d)
        # print(self.G.edges())

        color_map = {self.father: 'pink'}  # Создадим Словаь цветов вершин, которые мы хотим покрасить
        # values = [color_map.get(node, "Teal") for node in self.G.nodes()]# cоздаем словарь цветов для всех,
        # все остальные, кроме тех, что в списке выше, окрасятся green Кстати, это то же самое что и
        values = []
        for node in self.G.nodes():
            status = False
            for node_from_color_map in color_map.keys():
                if node_from_color_map == node:
                    values.append(color_map[node_from_color_map])
                    status = True
                    break
            if not status:
                values.append("Teal")
                """То есть values содержит цвета для вершину соотетственно
                списку вершин self.G.nodes(), типа словаря из двух массивов"""
        print(
            f"Список вершин {self.G.nodes()}\n\nUм соответсвуют \n\nCписок цветов {values}\n\nПолучится \n\n{dict(zip(self.G.nodes(), values))}")
        edge_labels = dict([((u, v,), d['weight'])
                            for u, v, d in self.G.edges(data=True)])

        posi = nx.spring_layout(self.G)
        nx.draw(self.G, pos=posi, node_color=values, node_size=1500,
                with_labels=True)  # цшер_дфиуды - отображать название, еще сюда из интересного можно вставить
        # edge_color=["r","b"] например,, это окрасит ребра
        nx.draw_networkx_edge_labels(self.G, posi, edge_labels=edge_labels)
        """ position, точно так
        же как и values приписывает графу положение x и y на координатной
        плоскости(не путать с координатами построения картинки self.h,
                  self.d, self.w)"""
        """с position не плохо справляется и встроенная в networkx логика"""
        path = f'{Graph._path}graph{time.time()}.png'
        plt.savefig(path)  # График оборачивается в картинку
        print('done')
        return GraphData(path, self.params)

    def frame_shot(self):  # Нарезка кадров от начала создания графа до создания последней вершины
        new = []  # Здесь будут храниться self.relations, постепенно заполняемые значениями
        images = []  # Здесь будут храниться наши снимки
        ps = nx.spring_layout(self.G)

        position_new = {}
        for element in self.relations:

            for x in ps.keys():
                if position_new != {}:
                    for y in position_new.keys():
                        condition = False
                        if y == x:
                            condition = True
                            break
                    if not condition:
                        position_new[x] = ps[x]
                else:
                    position_new[x] = ps[x]

            new.append(element)
            H = nx.Graph()
            plt.figure(figsize=(self.w, self.h), dpi=self.d)
            H.add_weighted_edges_from(new)  # По вершинам
            nx.draw(H, pos=position_new, node_size=700, with_labels=True)
            nx.draw_networkx_edge_labels(H, position_new)
            path = f'{Graph._path}buf.png'
            plt.savefig(path)
            images.append(imageio.imread(path))

        kargs = {'duration': 0.5}
        imageio.mimsave(f'{Graph._path}movie{time.time()}.gif', images, **kargs)
        print('done')


# d = [["Иного букв актер Вася",2,2],[2,5,1], [5,3, 2],[1,9,3],[2,12, 2],[5,12,1], [6,3, 2],[29,9,3],[470,12, 2],
# [125,12,1], [29,470,3],[470,29, 3],[125,470,1]] r = Graph(d) r.draw_graph() r.draw_transport(2,5) r.frame_shot() %%
import random


def express_test(d):
    # d = [["Иного букв актер Вася",2,2],[2,5,1], [5,3, 2],[1,9,3],[2,12, 2],[5,12,1], [6,3, 2],[29,9,3],[470,12, 2],
    # [125,12,1], [29,470,3],[470,29, 3],[125,470,1]]
    d = simulator(d)
    r = Graph(d, None)
    r.draw_graph()
    # r.draw_transport(2, 5)
    r.frame_shot()


def simulator(count, i=100):
    im = i * (-1)
    d = [[str(random.randint(im, i)), str(random.randint(im, i)), 1] for x in range(count)]
    return d


express_test(50)
