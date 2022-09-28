import numpy as np
import pandas as pd
from annoy import AnnoyIndex

from icecream import ic


def nan_in_0(x):
    """
    Замена NaN на 0
    """
    if str(x) == "nan":
        x = 0
    return x


def name_in_h(x):
    """
    Определение глубины по номеру пробы
    :param x: "ТСЗ-01/22,4-22,6"
    :return:  22.5
    """
    x = str(x)
    if x == "nan":
        y = 0
    else:
        y = round(
            np.mean(
                list(
                    map(float,
                        x.split("/")[1].replace(",", ".").split("-")
                        )
                )
            ),
            1
        )
    return y


df = pd.read_excel("data/stats_soil.xlsx")

w = np.array(list(map(nan_in_0, df["W"])))
wl = np.array(list(map(nan_in_0, df["WL"])))
wp = np.array(list(map(nan_in_0, df["WP"])))
p = np.array(list(map(nan_in_0, df["ρ"])))
h_list = np.array(list(map(name_in_h, df["N"])))

dataset = np.vstack([w, wl, wp, p, h_list]).T
"""
Создание пространства
"""
dimension = np.size(dataset, axis=1)  # Размерность данных
forest = 20  # Сколько деревьев использовать

Space = AnnoyIndex(dimension, metric='angular')
for i in range(len(h_list)):  # Добавление векторов в пространств
    Space.add_item(i, dataset[i])
Space.build(n_trees=forest, n_jobs=-1)  # После build нельзя добавлять вектора
"""
Поиск в пространстве
"""
find_near = 5  # Сколько найти соседий
for i in range(len(h_list)):
    point = dataset[i]
    neighbor = Space.get_nns_by_vector(point, find_near, search_k=-1)
    near_wl = []
    near_h = []
    for near in neighbor:
        near_wl.append(wl[near])
        near_h.append(h_list[near])
    x_array = np.array(near_wl)
    sigma = np.std(x_array)
    print(sigma, near_h)

