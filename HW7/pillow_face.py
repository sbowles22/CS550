from PIL import Image
from math import *

size = (100, 100)

file = Image.new('RGB', size)

for i in range(size[0]):
    for j in range(size[1]):
        file.putpixel((i, j), (255, 255, 255))

for i in (30, 70):
    for j in range(10, 60):
        file.putpixel((i, j), (0, 0, 0))

c = 0.3
i = 3*pi/4 - c
while i < 3*pi/4 + c:
    file.putpixel((int(30+50*cos(i)), int(50+50*sin(i))), (0, 0, 0))
    c += .1

file.save("test_image.png", 'PNG')