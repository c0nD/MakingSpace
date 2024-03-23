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