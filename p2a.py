from random import randint

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


def populate():
    population = []
    for i in range(POPULATION_SIZE):
        map = []
        for j in range(MAP_SIZE):
            map.append(randint(1,COLOR))
        population.append(map)
    return map


def main():
    population = populate()

if __name__ == "__main__":
    main()