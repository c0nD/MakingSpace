from panda3d.core import (NodePath, GeomNode, Geom, GeomVertexFormat, GeomVertexData,
                          GeomVertexWriter, GeomTriangles, PointLight, AmbientLight, Vec4,
                          Material, Plane, PlaneNode)
from direct.showbase.ShowBase import ShowBase
from direct.filter.CommonFilters import CommonFilters
from direct.task import Task
import random
import numpy as np
from panda3d.core import CardMaker
from Planet import Planet

class Star:

    def __init__(self, radius=1.0, pos=(0, 0, 0)):
        self.radius = radius
        self.position = pos
        self.node = self.create_star()


    def animate_light(self, task):
        # Sine wave for smooth pulsation
        pulsation_speed = 0.5  # adjust for faster or slower pulsation
        brightness = (np.sin(task.time * pulsation_speed) + 1) / 2  # normalized between 0 and 1

        # Update the light color and intensity
        light_color = Vec4(brightness, brightness, brightness, 1)
        self.star_light.setColor(light_color)

        return Task.cont


    def create_star(self):
        format = GeomVertexFormat.getV3n3c4()
        vdata = GeomVertexData("star", format, Geom.UHDynamic)

        vertex = GeomVertexWriter(vdata, "vertex")
        normal = GeomVertexWriter(vdata, "normal")
        color = GeomVertexWriter(vdata, "color")

        num_segments = 32

        for i in range(num_segments + 1):
            for j in range(num_segments + 1):
                theta = (i / num_segments) * 2 * np.pi
                phi = (j / num_segments) * np.pi

                x = self.radius * np.sin(phi) * np.cos(theta)
                y = self.radius * np.sin(phi) * np.sin(theta)
                z = self.radius * np.cos(phi)

                vertex.addData3f(x, y, z)
                normal.addData3f(x, y, z)
                color.addData4f(generate_random_star_color())

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
        node = GeomNode("star")
        node.addGeom(geom)

        star_node = NodePath(node)
        star_node.setPos(self.position)

        star_material = Material()
        star_material.setShininess(100)
        star_material.setEmission(Vec4(1, 1, 1, 1))
        star_node.setMaterial(star_material, 1)



        # Light emission
        star_light = PointLight('star_light')
        star_light.setColor((1, 1, 1, 1))
        # large light area to create a glow effect around the star 
        star_light.setAttenuation((0, 0.0001, 0.0001))
        star_light_node = star_node.attachNewNode(star_light)
        star_node.setLight(star_light_node)

        return star_node
    
    
def generate_random_star_color():
    r = random.uniform(0.8, 1.0)
    g = random.uniform(0.8, 1.0)
    b = random.uniform(0.8, 1.0)
    return r, g, b, 1.0


class StarApp(ShowBase):
    def __init__(self):
        super().__init__()

        # Set a darker background to contrast the bright star
        base.setBackgroundColor(0, 0, 0)

        # Create the star and keep a reference to the instance
        self.star_instance = Star(2.0, (0, 50, 0))
        star_node = self.star_instance.node
        star_node.reparentTo(self.render)

        # Assign the PointLight created in Star to an attribute for access
        self.star_instance.star_light = PointLight('star_light')
        self.star_instance.star_light.setColor((1, 1, 1, 1))
        self.star_instance.star_light.setAttenuation((0, 0.0001, 0.0001))
        star_light_node = star_node.attachNewNode(self.star_instance.star_light)
        star_node.setLight(star_light_node)

        # Add a task to animate the light
        self.taskMgr.add(self.star_instance.animate_light, "animate_light")
        

        # Enable bloom effect for glow
        filters = CommonFilters(base.win, base.cam)
        filters.setBloom(blend=(0, 0, 0, 1), mintrigger=0.5, maxtrigger=1.0, desat=0, intensity=1.0)
        # Add ground
        self.add_ground()

        # Add spheres around the star
        #self.add_spheres_around_star()
        self.add_planets_around_star()

    def add_ground(self):
        # Create a ground plane
        cm = CardMaker("ground")
        cm.setFrame(-100, 100, -100, 100)
        ground = NodePath(cm.generate())
        ground.setP(-90)  # Rotate to make it horizontal
        ground.setY(50)  # Positioning in front of the star
        ground.setZ(-10)  # Lower than the star
        ground.setColor((0.1, 0.1, 0.1, 1))
        ground.reparentTo(self.render)

    def add_spheres_around_star(self):
        # Add spheres with a simple material to reflect the star's light
        for _ in range(10):
            sphere = self.loader.loadModel("models/misc/sphere")
            sphere.reparentTo(self.render)
            sphere.setScale(2)  # Adjust size as necessary
            x = random.uniform(-50, 50)
            y = 50  # Keep them at the same depth as the star
            z = random.uniform(-50, 50)
            sphere.setPos(x, y, z)
            
            # Add a basic material to the spheres
            mat = Material()
            mat.setShininess(10)  # Adjust the shininess
            sphere.setMaterial(mat, 1)


    # adding some planets around it
    def add_planets_around_star(self):
        for i in range(5):
            planet = Planet(random.uniform(1, 5))
            planet.node.reparentTo(self.render)
            planet.node.setPos(random.uniform(-50, 50), 50, random.uniform(-50, 50))

if __name__ == '__main__':
    app = StarApp()
    app.run()