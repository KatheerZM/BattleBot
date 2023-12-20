import math
import random as rand
from data import terrain_map, borders, city_list

mean_city_density = 1


def is_city(x, y):
    return terrain_map[x][y] == 50


def is_free(x, y):
    return borders[x][y] == 0


def get_distance(coord_a, coord_b):
    return abs(coord_a[0] - coord_b[0]) + abs(coord_a[1] - coord_b[1])


def city_density(city_list, coord_a):
    count = 0
    for city in city_list:
        if get_distance(city, coord_a) < 30:
            count += 1
    return count / 30**2


def normalized_city_density(city_list, coord_a):
    global mean_city_density
    if mean_city_density == 1:
        mean_city_density = geo_mean(
            *[city_density(city_list, city) for city in city_list]
        )
    return city_density(city_list, coord_a) / mean_city_density


def geo_mean(*args):
    total = 0
    for arg in args:
        total += math.log10(arg)
    mean = 10 ** (total / len(args))
    return mean


def two_city_density(city_list, coord_a, coord_b):
    return geo_mean(
        normalized_city_density(city_list, coord_a),
        normalized_city_density(city_list, coord_b)
    )


def find_starting_city():
    far_distance = 180
    near_distance = 0
    ideal_min, ideal_mid, ideal_max = 38, 40, 42
    min_delta = (ideal_mid - near_distance) / 10
    max_delta = (far_distance - ideal_mid) / 20
    level = 0

    free_cities = []
    used_cities = []
    for city_x, city_y in city_list:
        if is_free(city_x, city_y):
            free_cities.append((city_x, city_y))
        else:
            used_cities.append((city_x, city_y))

    distances = []
    for free_coord in free_cities:
        min_dis, min_coord = 10000, (-1, -1)
        for used_coord in used_cities:
            dis = get_distance(free_coord, used_coord) * two_city_density(city_list, free_coord, used_coord)
            if dis < min_dis:
                min_dis, min_coord = dis, used_coord
        distances.append(min_dis)

    free_zipped = list(zip(distances, free_cities))
    free_zipped.sort()

    if len(free_cities) == 0:
        print("There are no free cities")
        return None
    if len(used_cities) == 0:
        print("Every city is free")
        return None, (57, 56)  # rand.choice(free_cities)

    while True:
        valid_choices = [f for f in free_zipped if ideal_min < f[0] < ideal_max]
        if not len(valid_choices) == 0:
            return rand.choice(valid_choices)
        ideal_max += max_delta
        level += 0.5
        valid_choices = [f for f in free_zipped if ideal_min < f[0] < ideal_max]
        if not len(valid_choices) == 0:
            return rand.choice(valid_choices)
        ideal_min -= min_delta
        level += 0.5


if __name__ == "__main__":
    while True:
        dis, (x, y) = find_starting_city()
        print(dis, x, y)
        borders[x][y] = 1