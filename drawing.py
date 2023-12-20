from PIL import Image, ImageDraw
import random as rand
from data import terrain_map, units, unit_key

SQUARE_SIZE = 50
VIEW_BOARD_SIZE = 9
mid_x_y = VIEW_BOARD_SIZE // 2


def draw_png_coord(img, png_names, coord):
    if png_names is None:
        return
    png_names = [png_names] if isinstance(png_names, str) else png_names
    for png_name in png_names:
        png_name = png_name + ".png" if ".png" not in png_name else png_name
        if "images/" not in png_name:
            png_name = "images/" + png_name
        x, y = coord
        top_left = (x * (SQUARE_SIZE + 1) + 1, y * (SQUARE_SIZE + 1) + 1)
        sprite_image = Image.open(png_name)
        if sprite_image.mode != 'RGBA':
            sprite_image = sprite_image.convert('RGBA')
        img.paste(sprite_image, (top_left[0], top_left[1]), sprite_image.split()[3])


def draw_color_coord(draw, color, coord, square_size=SQUARE_SIZE):
    x, y = coord
    top_left = (x * (square_size + 1) + 1, y * (square_size + 1) + 1)
    bottom_right = (top_left[0] + square_size - 1, top_left[1] + square_size - 1)
    draw.rectangle([top_left, bottom_right], fill=color)


special_sea_tiles = ["sea_tile_fish1", "sea_tile_fish2", "sea_tile_lily1"]
def get_sea_tile():
    if rand.random() < 0.7:
        return "sea_tile_v1"
    else:
        return special_sea_tiles[rand.randint(0, len(special_sea_tiles) - 1)]


terrain_key = {10: "grassland_v1",
               20: "sandy_desert_v1"}


def get_surrounding_terrain(sx, sy):
    delta = 1
    while True:
        try:
            if terrain_map[sx + delta][sy] // 10 in [1, 2]:
                return terrain_key[terrain_map[sx + delta][sy] // 10 * 10]
        except:
            pass
        try:
            if terrain_map[sx - delta][sy] // 10 in [1, 2]:
                return terrain_key[terrain_map[sx - delta][sy] // 10 * 10]
        except:
            pass
        try:
            if terrain_map[sx][sy + delta] // 10 in [1, 2]:
                return terrain_key[terrain_map[sx][sy + delta] // 10 * 10]
        except:
            pass
        try:
            if terrain_map[sx][sy - delta] // 10 in [1, 2]:
                return terrain_key[terrain_map[sx][sy - delta] // 10 * 10]
        except:
            pass
        delta += 1


def get_river_tile(sx, sy):
    tile_name = "river_"
    if terrain_map[sx][sy + 1] in [1, 2]:
        tile_name += "d"
    if terrain_map[sx + 1][sy] in [1, 2]:
        tile_name += "r"
    if terrain_map[sx][sy - 1] in [1, 2]:
        tile_name += "u"
    if terrain_map[sx - 1][sy] in [1, 2]:
        tile_name += "l"
    tile_name += "_v1"
    return tile_name


def get_square_tile(sx, sy):
    tvalue = terrain_map[sx][sy]
    if tvalue == 1:
        return get_sea_tile()
    elif tvalue == 2:
        return [get_surrounding_terrain(sx, sy),
                get_river_tile(sx, sy)]
    elif tvalue == 10:
        return "grassland_v1"
    elif tvalue == 11:
        return ["grassland_v1", "mountains_v1"]
    elif tvalue == 12:
        return ["forest_v1"]
    elif tvalue == 20:
        return ["sandy_desert_v1"]
    elif tvalue == 21:
        return ["sandy_desert_mountain_v1"]
    elif tvalue == 50:
        return ["city_v1"]


def get_square_unit(sx, sy):
    unit_info = units[sx][sy]
    if unit_info == 0:
        return None
    team, unit, moves, last_addition = unit_info
    return unit_key[unit][1]


def generate_board(position, square_size=SQUARE_SIZE, board_size=VIEW_BOARD_SIZE):
    # Calculate the total image size including black lines
    img_size = board_size * square_size + (board_size - 1)

    # Create a white image
    img = Image.new('RGB', (img_size, img_size), color='white')
    draw = ImageDraw.Draw(img)

    # Draw black lines for the grid
    for i in range(board_size):
        # Horizontal line
        draw.line([(0, i * (square_size + 1)), (img_size, i * (square_size + 1))], fill='black')
        # Vertical line
        draw.line([(i * (square_size + 1), 0), (i * (square_size + 1), img_size)], fill='black')

    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    px, py = position
    # TILES
    for dx in range(-mid_x_y, board_size - mid_x_y):
        for dy in range(-mid_x_y, board_size - mid_x_y):
            if px + dx >= len(terrain_map[0]) or py + dy >= len(terrain_map):
                continue
            elif px + dx < 0 or py + dy < 0:
                continue
            draw_png_coord(img,
                           get_square_tile(px + dx, py + dy),
                           (dx + mid_x_y, dy + mid_x_y))
            draw_png_coord(img,
                           get_square_unit(px + dx, py + dy),
                           (dx + mid_x_y, dy + mid_x_y))
    # SPRITES
    # draw_color_coord(draw, "green", (mid_x_y, mid_x_y))
    # draw_png_coord(img, "flag_horse_v1", (mid_x_y, mid_x_y))

    # Save the image
    img.save('images/board.png')
    return img