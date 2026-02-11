import os
import shutil
from PIL import Image

templates_dir = os.path.join(os.path.dirname(__file__), 'templates')


def make_thumbnail(section_name, original='original.jpg'):
    path = os.path.join(templates_dir, section_name)
    size = 240*2, 148*2
    listdir = filter(str.isdigit, os.listdir(path))
    for item_id in listdir:
        print "Converting thumbnail: " + section_name + "/" + item_id
        src = os.path.join(path, item_id, original)
        dst = os.path.join(path, item_id, 'thumbnail.jpg')
        if os.path.isfile(dst):
            os.remove(dst)
        im = Image.open(src)
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(dst, "JPEG")


def make_pic(section_name):
    path = os.path.join(templates_dir, section_name)
    size = 720*2, 745*2
    listdir = filter(str.isdigit, os.listdir(path))
    for item_id in listdir:
        print "Converting full pic: " + section_name + "/" + item_id
        src = os.path.join(path, item_id, 'original_full.jpg')
        dst = os.path.join(path, item_id, 'full.jpg')
        if os.path.isfile(dst):
            os.remove(dst)
        im = Image.open(src)
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(dst, "JPEG")


def make_comics(section_name):
    path = os.path.join(templates_dir, section_name)
    size = 970*2, 1400*2
    listdir = filter(str.isdigit, os.listdir(path))
    for item_id in listdir:
        comics_dir = os.path.join(path, item_id)
        for comics_pic in os.listdir(comics_dir):
            if comics_pic.startswith("original_") and comics_pic.endswith(".jpg"):
                print "Converting comics pic: " + section_name + "/" + item_id + "/" + comics_pic
                src = os.path.join(path, item_id, comics_pic)
                dst = os.path.join(path, item_id, comics_pic.replace("original_", ""))
                if os.path.isfile(dst):
                    os.remove(dst)
                im = Image.open(src)
                im.thumbnail(size, Image.ANTIALIAS)
                im.save(dst, "JPEG")


make_thumbnail('princess')
make_thumbnail('princess_seasons')
make_thumbnail('cartoons')
make_thumbnail('comics')
make_thumbnail('misc')

make_thumbnail('projects', 'original_thumb.jpg')
make_thumbnail('flat', 'original_thumb.jpg')

make_pic('projects')
make_pic('flat')

make_comics('comics')
