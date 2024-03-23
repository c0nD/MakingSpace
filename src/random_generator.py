import random
import math

# nodePath.setColor(r, g, b, a)

def generate_random_color() -> tuple:
    """
    Generates a random color.
    returns a tuple representing the color.
    """
    r = random.random()
    g = random.random()
    b = random.random()
    a = 1.0
    return r, g, b, a


def generate_random_star_color() -> tuple:
    """
    Generates a random color for a star.
    returns a tuple representing the color -- specifically, a yellowish color.
    """
    r = random.random()
    g = random.random() - 0.5
    b = 0.0
    a = 1.0
    return r, g, b, a