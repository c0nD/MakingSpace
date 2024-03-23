import random
from panda3d.core import Color4


def generate_random_color():
    return Color4(random.random(), random.random(), random.random(), 1)


def generate_random_red():
    return Color4(random.random(), 0, 0, 1)

def generate_random_green():
    return Color4(0, random.random(), 0, 1)


def generate_random_blue():
    return Color4(0, 0, random.random(), 1)