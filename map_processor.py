import random as rand
import numpy as np
from PIL import Image, ImageDraw

sea_map = []
im = Image.open("images/map_v1.png")
im = im.convert('RGB')
x, y = im.size
x //= 4
y //= 4
for j in range(y):
    sea_map.append([])
    for i in range(x):
        i4, j4 = i * 4, j * 4
        if im.getpixel((i4, j4)) == (66, 173, 255):
            sea_map[j].append(1)
        elif im.getpixel((i4, j4 + 1)) == (66, 173, 255):
            sea_map[j].append(1)
        elif im.getpixel((i4 + 1, j4 + 1)) == (66, 173, 255):
            sea_map[j].append(1)
        elif im.getpixel((i4 + 1, j4)) == (66, 173, 255):
            sea_map[j].append(1)
        else:
            sea_map[j].append(0)

sea_map_rgb = [[(66, 173, 255) if p == 1 else (255, 255, 255) for p in row] for row in sea_map]
sea_map_rgb = np.array(sea_map_rgb, dtype=np.uint8)
print(sea_map_rgb.shape)
image = Image.fromarray(sea_map_rgb, 'RGB')
image.show()
image.save('map_v3.png')

exit()

sea_map = []
im = Image.open("images/europe_map.jpg")

x, y = im.size
for j in range(y):
    sea_map.append([])
    for i in range(x):
        r, g, b = im.getpixel((i, j))
        if b > r + 20 and b > g + 20:
            sea_map[j].append(1)
        else:
            sea_map[j].append(0)

sea_map_rgb = [[(80, 80, 255) if p == 1 else (255, 255, 255) for p in row] for row in sea_map]
sea_map_rgb = np.array(sea_map_rgb, dtype=np.uint8)
print(sea_map_rgb.shape)
image = Image.fromarray(sea_map_rgb, 'RGB')
image.show()
image.save('output_image.png')
print()