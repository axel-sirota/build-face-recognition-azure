import os
from PIL import Image

try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO


from PIL import Image


def save_image(filename):
    print(f"Dealing with {filename}")
    if filename != ".DS_Store":
        im1 = Image.open(f'backup/{filename}')
        im1.save(f'images/{filename}', "JPEG", quality=25)


for filename in os.listdir("backup"):
    save_image(filename)
