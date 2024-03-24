import random
from panda3d.core import NodePath, Material, GeomNode, Geom, GeomVertexFormat, GeomVertexData, GeomVertexWriter, GeomTriangles, CardMaker, TransparencyAttrib
from direct.showbase.ShowBase import ShowBase
import math
import numpy as np


# https://discourse.panda3d.org/t/procedurally-generating-3d-models/14623/4
class Planet:

    def __init__(self, radius=1.0, pos=(0, 0, 0), has_rings=False, ring_color=(1, 1, 1, 0.5)):
        self.radius = radius
        self.position = pos
        self.has_rings = has_rings
        self.ring_color = ring_color
        self.node = NodePath("planet_node")
        self.base_color = generate_planet_color()  # Generate a base color for the planet
        self.create_planet()
        if self.has_rings:
            self.create_rings()


    def create_planet(self):
        format = GeomVertexFormat.getV3n3c4()
        vdata = GeomVertexData("planet", format, Geom.UHDynamic)

        vertex = GeomVertexWriter(vdata, "vertex")
        normal = GeomVertexWriter(vdata, "normal")
        color = GeomVertexWriter(vdata, "color")


        num_segments = 32

        # Generate vertices for the planet
        for i in range(num_segments + 1):
            for j in range(num_segments + 1):
                theta = (i / num_segments) * 2 * math.pi
                phi = (j / num_segments) * math.pi

                x = self.radius * math.sin(phi) * math.cos(theta)
                y = self.radius * math.sin(phi) * math.sin(theta)
                z = self.radius * math.cos(phi)

                vertex.addData3f(x, y, z)
                normal.addData3f(x, y, z)

                color_variation = (random.uniform(-0.05, 0.05) for _ in range(3))
                varied_color = tuple(min(max(bc + cv, 0), 1) for bc, cv in zip(self.base_color[:3], color_variation))
                color.addData4f(*varied_color, 1.0)  # Add alpha value of 1

        # Generate triangles
        prim = GeomTriangles(Geom.UHDynamic)
        for i in range(num_segments):
            for j in range(num_segments):
                next_i = (i + 1)
                next_j = (j + 1)

                i0 = i * (num_segments + 1) + j
                i1 = i * (num_segments + 1) + next_j
                i2 = next_i * (num_segments + 1) + j
                i3 = next_i * (num_segments + 1) + next_j

                prim.addVertices(i0, i2, i1)
                prim.addVertices(i1, i2, i3)

        prim.closePrimitive()
        geom = Geom(vdata)
        geom.addPrimitive(prim)
        node = GeomNode("planet")
        node.addGeom(geom)

        planet_material = Material()
        planet_material.setShininess(100)
        planet_material.setEmission(self.base_color)

        planet_np = NodePath(node)
        planet_np.setMaterial(planet_material, 1)
        planet_np.reparentTo(self.node)
        planet_np.setPos(*self.position)


    def create_rings(self, segments=100, color=(1, 0.9, 0.8, 0.3)):
        """
        Creates rings around the planet with specified parameters.
        """
        inner_radius = self.radius * 1.2
        outer_radius = self.radius * 1.5

        format = GeomVertexFormat.getV3n3c4()
        vdata = GeomVertexData('rings', format, Geom.UHDynamic)
        vertex = GeomVertexWriter(vdata, 'vertex')
        normal = GeomVertexWriter(vdata, 'normal')
        color_writer = GeomVertexWriter(vdata, 'color')

        for i in range(segments + 1):
            angle = 2 * np.pi * i / segments
            for radius in (inner_radius, outer_radius):
                x = radius * np.cos(angle)
                y = radius * np.sin(angle)
                z = 0  # equatorial shape, so z is constant
                
                vertex.addData3f(x, y, z)
                normal.addData3f(0, 0, 1)  # normal points along the z-axis
                color_writer.addData4f(*color)

        # Create the triangles
        prim = GeomTriangles(Geom.UHDynamic)
        for i in range(segments):
            start_index = i * 2
            prim.addVertices(start_index, start_index + 1, start_index + 3)
            prim.addVertices(start_index, start_index + 3, start_index + 2)

        geom = Geom(vdata)
        geom.addPrimitive(prim)
        node = GeomNode('ring_node')
        node.addGeom(geom)
        ring_node = NodePath(node)
        ring_node.reparentTo(self.node)  # attach to planet's node

        ring_node.setPos(*self.position)
        
def generate_random_color() -> tuple:
    r = random.random()
    g = random.random()
    b = random.random()
    a = 1.0
    return r, g, b, a


def generate_planet_color():
    """
    Generates more realistic planet colors.
    """
    colors = [
        (0.2, 0.5, 1.0, 1),  # Earth-like blue
        (1.0, 0.5, 0.2, 1),  # Mars-like red
        (0.9, 0.8, 0.7, 1),  # Venus-like yellow
        (0.5, 0.3, 0.0, 1),  # Mercury-like brown
        (0.9, 0.9, 0.9, 1),   # Moon-like gray,
        generate_random_color(),
    ]
    return random.choice(colors)


if __name__ == '__main__':
    app = ShowBase()
    planet = Planet(2.0, pos=(0, 50, 0), has_rings=True, ring_color=(1, 0.9, 0.8, 0.3)).node
    planet.reparentTo(app.render)
    app.run()