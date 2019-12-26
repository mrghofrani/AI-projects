from random import randint, choices
from itertools import chain

POPULATION_SIZE = 20
MAP_SIZE = 31
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
    "South Korasan": ["Razavi Khorasan", "Semnan", "Isfahan", "Yazd", "Kerman", "Sistan and Baluchestan"],
    "Yazd": ["Isfahan", "South Khorasan", "Kerman", "Fars"],
    "Fars": ["Yazd", "Isfahan", "Kohgiluyeh and Boyer-Ahmad", "Bushehr", "Hormozgan", "Kerman"],
    "Kohgiluyeh and Boyer-Ahmad": ["Fars", "Isfahan", "Chaharmahal and Bakhtiari", "Khuzestan", "Bushehr"],
    "Chaharmahal and Bakhtiary": ["Isfahan", "Kohgiluyeh and Boyer-Ahmad", "Khuzestan", "Lorestan"],
    "Khuzestan": ["Bushehr", "Kohgiluyeh and Boyer-Ahmad", "Chaharmahal and Bakhtiari", "Lorestan", "Ilam"],
    "Ilam": ["Khuzestan", "Lorestan", "Kermanshah"],
    "Lorestan": ["Ilam", "Kermanshah", "Hamedan", "Markazi", "Isfahan", "Chaharmahal and Bakhtiari", "Khuzestan"],
    "Bushehr": ["Khuzestan", "Kohgiluyeh and Boyer-Ahmad", "Fars", "Hormozgan"],
    "Hormozgan": ["Bushehr", "Fars", "Kerman", "Sistan and Baluchestan"],
    "Kerman": ["Fars", "Yazd", "South Khorasan", "Sistan and Baluchestan", "Hormozgan"],
    "Sistan and Baluchestan": ["Hormozgan", "Kerman", "South Khorasan"]
}
COLOR = 4
M = lambda: len(list(chain(*IRAN_MAP.values())))/2
TORNUMENT_SIZE = 2

class Map:
    def __init__(self, colored_map, fitness=None):
        self.cmap = colored_map
        self.fitness = fitness

    def calculate_fitness(self):
        sigma_sum = 0
        for city in IRAN_MAP:
            sigma = 1
            city_color = self.cmap[city]
            for adj in IRAN_MAP[city]:
                if city_color == self.cmap[adj]:
                    sigma = 0
                    break
            sigma_sum += sigma
        self.fitness = sigma_sum / M
    
            
def populate():
    population = []
    for _ in range(POPULATION_SIZE):
        colored_map = dict()
        for city in IRAN_PROVINCES:
            colored_map[city] = randint(1,COLOR)
        population.append(Map(colored_map))
    return population


def fitness_function(population):
    for element in population:
        element.calculate_fitness()


def select_parents(population):
    parent = []
    for i in range(POPULATION_SIZE // 2):
        tmp_parent = choices(population, k=TORNUMENT_SIZE)
        dominant_parent = max(tmp_parent, key=lambda p: p.fitness)
        parent.append(dominant_parent)
    return parent


def crossover(parent, p1, p2):
    cross_point = MAP_SIZE // 2
    p1_cmap = parent[p1].colored_map[:]
    p2_cmap = parent[p2].colored_map[:]
    p1_cmap[:cross_point], p2_cmap[cross_point+1:] = p2_cmap[:cross_point], p1_cmap[cross_point+1:]
    return Map(p1_cmap), Map(p2_cmap)

def generate_new_population(parent):
    population = []
    visited = []
    p1 = float("inf")
    p2 = float("inf")
    for i in range(POPULATION_SIZE // 2):
        while p1 in visited:
            p1 = randint(0, POPULATION_SIZE // 2 - 1)
        visited.append(p1)
        while p2 in visited:
            p2 = randint(0, POPULATION_SIZE // 2 - 1)
        visited.append(p2)
        child1, child2 = crossover(parent, p1, p2)
        population.append(child1)
        population.append(child2)
    return population


def main():
    population = populate()
    fitness_function(population)
    parents = select_parents(population)
    population = generate_new_population(parents)



if __name__ == "__main__":
    main()