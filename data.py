from PIL import Image
import ast


# Load map
terrain_map = []
map_im = Image.open("images/map_v2.png")
map_im = map_im.convert('RGB')
y, x = map_im.size
map_x, map_y = x, y
map_size = (map_x, map_y)
for j in range(y):
    terrain_map.append([])
    for i in range(x):
        rgb = map_im.getpixel((j, i))
        if rgb == (66, 173, 255):  # Light blue
            terrain_map[j].append(1)

        elif rgb == (0, 111, 255):  # Dark blue
            terrain_map[j].append(2)

        elif rgb == (255, 255, 255):  # White
            terrain_map[j].append(10)

        elif rgb == (96, 96, 96):  # Dark Gray
            terrain_map[j].append(11)

        elif rgb == (56, 188, 0):  # Dark green
            terrain_map[j].append(12)

        elif rgb == (255, 216, 0):  # Yellow
            terrain_map[j].append(20)

        elif rgb == (155, 129, 0):  # Dark Yellow
            terrain_map[j].append(21)

        elif rgb == (255, 0, 0):  # City
            terrain_map[j].append(50)

city_list = [(x, y) for x in range(len(terrain_map))
             for y in range(len(terrain_map[0]))
             if terrain_map[x][y] == 50]


try:
    with open("data/units.txt", "r") as file_unit:
        line = file_unit.readlines()[0]
        units = ast.literal_eval(line)
except:
    units = []
    for row in terrain_map:
        units.append([])
        for item in row:
            units[-1].append(0)
    with open("data/units.txt", "a") as file_unit:
        file_unit.writelines(str(units))

try:
    with open("data/players.txt", "r") as file_unit:
        line = file_unit.readlines()[0]
        players = ast.literal_eval(line)
except:
    players = [0]
    with open("data/players.txt", "a") as file_unit:
        file_unit.writelines(str(players))

unit_key = {
    #  (name, png, max_move, attack, defense, is_ranged, range, ranged)
    1: ("Sword Infantry", "swordman_v1", 4, 10, 12, 0, 0, 0),
    2: ("Spear Infantry", "spearman_v1", 4, 8, 20, 0, 0, 0),
    3: ("Cavalry", "horseman_v3", 6, 15, 6, 0, 0, 0),
    4: ("Archers", "bowman_v1",   4, 3, 6, 1, 3, 8),
    5: ("Flag Infantry", "flag_foot_v1", 4, 10, 12, 0, 0, 0),
    6: ("Flag Cavalry", "flag_horse_v1", 6, 15, 6, 0, 0, 0),
}
unit_unique_id = 0
units_by_team = {}
for x, row in enumerate(units):
    for y, unit in enumerate(row):
        if not unit == 0:
            team, unit, moves, last_add = unit
            if team not in units_by_team:
                units_by_team[team] = []
            units_by_team[team].append([(x, y), unit, moves, last_add, unit_unique_id])
            unit_unique_id += 1


def unit_to_border(team_id, team_unit):
    # [team, unit, moves, last_addition]
    (x, y), unit, moves, last_add, unique_id = team_unit
    return (x, y), [team_id, unit, moves, last_add]


def unit_from_id(team_id, unique_id):
    for unit in units_by_team[team_id]:
        if unit[4] == unique_id:
            return unit
    return -1


def unit_id_from_id(team_id, unique_id):
    for i, unit in enumerate(units_by_team[team_id]):
        if unit[4] == unique_id:
            return i
    return -1


def delete_unit_from_id(team_id, unique_id):
    units_by_team[team_id].pop(unit_id_from_id(team_id, unique_id))


def unit_to_team_deprecated(coord, border_unit):
    # (x, y), unit, moves, last_add
    team_id, unit, moves, last_add = border_unit
    return team_id, [coord, unit, moves, last_add]


try:
    with open("data/borders.txt", "r") as file_unit:
        line = file_unit.readlines()[0]
        borders = ast.literal_eval(line)
except:
    borders = []
    for row in terrain_map:
        borders.append([])
        for item in row:
            borders[-1].append(0)
    with open("data/borders.txt", "a") as file_unit:
        file_unit.writelines(str(borders))


def move_unit_by_team(team_id, unit_id, new_coord):
    new_x, new_y = new_coord
    old_x, old_y = units_by_team[team_id][unit_id][0]
    units[old_x][old_y], units[new_x][new_y] = 0, units[old_x][old_y]
    units_by_team[team_id][unit_id][0] = new_x, new_y


def place_unit(coord, info):
    global unit_unique_id
    px, py = coord
    units[px][py] = info
    team_id = info[0]
    if team_id not in units_by_team:
        units_by_team[team_id] = []
    units_by_team[team_id].append([
        (px, py),
        *info[1:],
        unit_unique_id
    ])
    unit_unique_id += 1
