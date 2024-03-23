from panda3d.core import NodePath, GeomNode, Geom, GeomVertexFormat, GeomVertexData, GeomVertexWriter, GeomTriangles
from direct.showbase.ShowBase import ShowBase
from random_generator import generate_random_color
import math


# https://discourse.panda3d.org/t/procedurally-generating-3d-models/14623/4
class Planet:

    def __init__(self, radius=1.0, pos=(0, 0, 0)):
        self.radius = radius
        self.node = self.create()


    def create(self):
        """
        Generates a planet with the given radius and returns a NodePath representing the planet.
        """
        format = GeomVertexFormat.getV3n3c4()
        vdata = GeomVertexData("planet", format, Geom.UHDynamic)

        vertex = GeomVertexWriter(vdata, "vertex")
        normal = GeomVertexWriter(vdata, "normal")
        color = GeomVertexWriter(vdata, "color")

        num_segments = 32  # The more segments, the smoother the sphere

        # Generate vertices
        for i in range(num_segments + 1):
            for j in range(num_segments + 1):
                theta = (i / num_segments) * 2 * math.pi
                phi = (j / num_segments) * math.pi

                x = self.radius * math.sin(phi) * math.cos(theta)
                y = self.radius * math.sin(phi) * math.sin(theta)
                z = self.radius * math.cos(phi)

                vertex.addData3f(x, y, z)
                normal.addData3f(x, y, z)  # Assuming sphere centered at origin; normals are the same as vertices
                color.addData4f(generate_random_color())

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

        return NodePath(node)


class PlanetApp(ShowBase):
    def __init__(self):
        super().__init__()
        planet = Planet(2.0).node
        planet.reparentTo(self.render)
        planet.setPos(0,50,0)

if __name__ == "__main__":
    app = PlanetApp()
    app.run()