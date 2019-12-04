from time import time
from PIL import Image, ImageFilter
from progressbar import progressbar
from numpy import interp

file = Image.open('flowers.jpg')
sunset = Image.open('sunset.jpg')

size = file.size
file = file.resize((1000, int(1000 * size[1]/size[0])))
size = file.size
sunset = sunset.resize(size)

for i in progressbar(range(size[0])):
    for j in range(size[1]):
        col = file.getpixel((i, j))
        if col[2] > 100 and col[1] < 100 and col[0] < 100:
            file.putpixel((i, j), (0, 0, 0))
        else:
            file.putpixel((i, j), (255, 255, 255))

file = Image.composite(Image.new('RGB', size), sunset, file.convert('L').filter(ImageFilter.GaussianBlur(2)))

file.save(f'img1.jpg', 'JPEG')