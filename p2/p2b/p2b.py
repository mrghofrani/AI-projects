from random import random, randint, choice
from math import exp, log
from itertools import chain
import sys
# The followings are needed for drawing diagram
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd



IRAN_PROVINCES = ["Alborz", "Ardabil", "East Azerbaijan", "West Azerbaijan", "Bushehr", "Chaharmahal and Bakhtiari", "Fars", "Gilan", "Golestan", "Hamedan", "Hormozgan", "Ilam", "Isfahan", 
                "Kerman", "Kermanshah", "North Khorasan", "Razavi Khorasan", "South Khorasan", "Khuzestan", "Kohgiluyeh and Boyer-Ahmad", "Kurdistan", "Lorestan", "Markazi", "Mazandaran",
                "Qazvin", "Qom", "Semnan", "Sistan and Baluchestan", "Tehran", "Yazd", "Zanjan"]
IRAN_MAP = {
    "West Azerbaijan": ["East Azerbaijan", "Zanjan", "Kurdistan"],
    "East Azerbaijan": ["West Azerbaijan", "Ardabil", "Zanjan"],
    "Ardabil": ["East Azerbaijan", "Zanjan", "Gilan"],
    "Gilan": ["Ardabil", "Zanjan", "Qazvin", "Mazandaran"],
    "Mazandaran": ["Gilan", "Qazvin", "Alborz", "Tehran", "Semnan", "Golestan"],
    "Golestan": ["Mazandaran", "Semnan", "North Khorasan"],
    "North Khorasan": ["Golestan", "Semnan", "Razavi Khorasan"],
    "Razavi Khorasan": ["North Khorasan", "Semnan", "South Khorasan"],
    "Semnan": ["Razavi Khorasan", "North Khorasan", "Golestan", "Mazandaran", "Tehran", "Qom", "Isfahan", "South Khorasan"],
    "Tehran": ["Alborz", "Mazandaran", "Semnan", "Qom", "Markazi"],
    "Alborz": ["Qazvin", "Mazandaran", "Tehran", "Qom", "Markazi"],
    "Qazvin": ["Gilan", "Mazandaran", "Alborz", "Markazi", "Hamedan", "Zanjan"],
    "Zanjan": ["Kurdistan", "West Azerbaijan", "East Azerbaijan", "Ardabil", "Gilan", "Qazvin", "Hamedan"],
    "Kurdistan": ["West Azerbaijan", "Zanjan", "Hamedan", "Kermanshah"],
    "Kermanshah": ["Kurdistan", "Hamedan", "Lorestan", "Ilam"],
    "Hamedan": ["Kermanshah", "Kurdistan", "Zanjan", "Qazvin", "Markazi", "Lorestan", "Kermanshah"],
    "Markazi": ["Hamedan", "Qazvin", "Alborz", "Tehran", "Qom", "Isfahan", "Lorestan"],
    "Qom": ["Markazi", "Tehran", "Semnan", "Isfahan"],
    "Isfahan": ["Qom", "Semnan", "South Khorasan", "Yazd", "Fars", "Kohgiluyeh and Boyer-Ahmad", "Chaharmahal and Bakhtiari", "Lorestan", "Markazi"],
    "South Khorasan": ["Razavi Khorasan", "Semnan", "Isfahan", "Yazd", "Kerman", "Sistan and Baluchestan"],
    "Yazd": ["Isfahan", "South Khorasan", "Kerman", "Fars"],
    "Fars": ["Yazd", "Isfahan", "Kohgiluyeh and Boyer-Ahmad", "Bushehr", "Hormozgan", "Kerman"],
    "Kohgiluyeh and Boyer-Ahmad": ["Fars", "Isfahan", "Chaharmahal and Bakhtiari", "Khuzestan", "Bushehr"],
    "Chaharmahal and Bakhtiari": ["Isfahan", "Kohgiluyeh and Boyer-Ahmad", "Khuzestan", "Lorestan"],
    "Khuzestan": ["Bushehr", "Kohgiluyeh and Boyer-Ahmad", "Chaharmahal and Bakhtiari", "Lorestan", "Ilam"],
    "Ilam": ["Khuzestan", "Lorestan", "Kermanshah"],
    "Lorestan": ["Ilam", "Kermanshah", "Hamedan", "Markazi", "Isfahan", "Chaharmahal and Bakhtiari", "Khuzestan"],
    "Bushehr": ["Khuzestan", "Kohgiluyeh and Boyer-Ahmad", "Fars", "Hormozgan"],
    "Hormozgan": ["Bushehr", "Fars", "Kerman", "Sistan and Baluchestan"],
    "Kerman": ["Fars", "Yazd", "South Khorasan", "Sistan and Baluchestan", "Hormozgan"],
    "Sistan and Baluchestan": ["Hormozgan", "Kerman", "South Khorasan"]
}
COLOR = 4
ALPHA = 0.9
T0 = 1
EPSILON = 0.001
M = len(list(chain(*IRAN_MAP.values())))/2
population_statistics = []


class Map:
    def __init__(self, colored_map, fitness=None):
        self.cmap = colored_map
        self.fitness = fitness
        self.calculate_fitness()

    def calculate_fitness(self):
        sigma_sum = 0
        for city in IRAN_MAP:
            city_color = self.cmap[city]
            for adj in IRAN_MAP[city]:
                sigma_sum += 1 if city_color != self.cmap[adj] else 0
        self.fitness = sigma_sum / M


def generate_state():
    colored_map = dict()
    for city in IRAN_PROVINCES:
        colored_map[city] = randint(1,COLOR)
    return Map(colored_map)


def successor(state):
    cmap = state.cmap.copy()
    city = choice(IRAN_PROVINCES)
    color = randint(1, COLOR)
    cmap[city] = color
    return Map(cmap)


def simulated_annealing(state, schedule):
    global population_statistics
    curr = state
    k = 0
    while True:
        T = schedule(k)
        population_statistics.append((T,curr.fitness))
        if T < EPSILON:
            return curr
        adj = successor(curr)
        delta_E = adj.fitness - curr.fitness
        if delta_E >= 0:
            curr = adj
        else:
            p = exp(delta_E / T)
            if p > random():
                curr = adj
        k += 1
        


def main():
    global population_statistics, EPSILON
    state = generate_state()
    schedule ={
        '1': lambda k: T0 * ALPHA**k,
        '2': lambda k: T0 / (1 + ALPHA * log(1 + k)),
        '3': lambda k: T0 / (1 + ALPHA * k),
        '4': lambda k: T0 / (1 + ALPHA * k**2)
    }
    run_mode = int(input("(0)User mode, (1)calculation mode:"))
    if run_mode == 0:
        c = input("Run with algorithm: (1 to 4) ")
        simulated_annealing(state, schedule[c])
        for val in population_statistics:
            print(val)
    elif run_mode == 1:
        global ALPHA, T0
        # storing min values in a new list
        for sched in schedule:
            if int(sched) == 1:
                alpha_set = np.arange(0.8, 0.9, 0.01).tolist()
                t0_set = [1, 10, 100, 1000, 10000]
                EPSILON = 0.001
            elif int(sched) == 2:
                alpha_set = [10, 100, 1000]
                t0_set = np.arange(1, 5, 1).tolist()
            else:
                alpha_set = [1, 10, 100, 1000, 10000]
                t0_set = [1, 10, 100, 1000, 10000]
                EPSILON = 0.001
            for ALPHA in alpha_set:
                for T0 in t0_set:
                    if int(sched) == 2:
                         EPSILON = 0.01 * T0
                    print(f"Running for sched#{int(sched)} T0={T0}, ALPHA={ALPHA}")
                    population_statistics = []
                    simulated_annealing(state, schedule[sched])

                    temperature = []
                    fitness = []
                    for pair in population_statistics:
                        temperature.append(pair[0])
                        fitness.append(pair[1])
                    df = pd.DataFrame({'x': list(range(1, len(population_statistics)+1)), 
                                    'y': fitness 
                                    }) 
                    plt.plot( 'x', 'y', data=df, marker='o', color='blue', linewidth=2, label="fitness")
                    plt.legend()
                    plt.savefig(f"./figure-1/sched#{int(sched)},T0#{T0},alpha#{ALPHA}.png")
                    plt.clf()


if __name__ == "__main__":
    main() 