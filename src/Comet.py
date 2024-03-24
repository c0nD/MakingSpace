from panda3d.core import (NodePath, GeomNode, Geom, GeomVertexFormat, GeomVertexData, GeomPoints, AmbientLight,
                            GeomVertexWriter, GeomTriangles, Vec4, Material, Plane, PlaneNode,
                            RenderModeAttrib, TransparencyAttrib, ColorBlendAttrib, PointLight, Material)
from panda3d.core import NodePath, Material, GeomNode, Geom, GeomVertexFormat, GeomVertexData, GeomVertexWriter, GeomTriangles, CardMaker, TransparencyAttrib
import random
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
import numpy as np
from collections import deque


class Comet:

    def __init__(self, radius=10, pos=(0,0,0), velocity=(0.1,0,0)):
        self.radius = radius
        self.position = pos
        self.velocity = velocity
        self.node = NodePath('comet_node')
        self.trail_node = NodePath('trail_node')

        self.comet_light = PointLight('comet_light')
        self.comet_light.setColor(Vec4(0.5, 0.5, 1, 1))
        self.comet_light_node = self.node.attachNewNode(self.comet_light)
        render.setLight(self.comet_light_node)
        
        self.comet_light.setAttenuation((1, 0, 0.01))

        self.node.reparentTo(render)
        self.trail_node.reparentTo(self.node)
        self.node.setPos(*self.position)

        self.create_comet()

        self.trail_particles = []

    
    def create_comet(self):
        format = GeomVertexFormat.getV3n3c4()
        vdata = GeomVertexData("comet", format, Geom.UHDynamic)
        vertex = GeomVertexWriter(vdata, "vertex")
        normal = GeomVertexWriter(vdata, "normal")
        color = GeomVertexWriter(vdata, "color")

        # Making sphere for the comet's 'core'
        for i in range(10):
            x = self.radius * random.uniform(-1, 1)
            y = self.radius * random.uniform(-1, 1)
            z = self.radius * random.uniform(-1, 1)

            vertex.addData3f(x, y, z)
            normal.addData3f(x, y, z)
            color.addData4f(0.5, 0.5, 1, 1)  # light blue

        # Making the trail
        points = GeomPoints(Geom.UHDynamic)
        points.addNextVertices(10)
        points.closePrimitive()

        geom = Geom(vdata)
        geom.addPrimitive(points)
        node = GeomNode("comet")
        node.addGeom(geom)

        comet_material = Material()
        comet_material.setShininess(100)
        comet_material.setEmission(Vec4(0.5, 0.5, 1, 1))  # light blue glow
        comet_node = NodePath(node)
        comet_node.setPos(*self.position)
        comet_node.setMaterial(comet_material, 1)

        return comet_node
    

    def create_trail_particle(self):
        # Geometry for the comet's trail particle -- doesnt look great but its fine lmao
        format = GeomVertexFormat.getV3n3c4()
        vdata = GeomVertexData("trail_particle", format, Geom.UHDynamic)
        vertex = GeomVertexWriter(vdata, "vertex")
        color = GeomVertexWriter(vdata, "color")

        vertex.addData3f(0, 0, 0)
        color.addData4f(0.5, 0.5, 1, 1)  # Light blue color

        points = GeomPoints(Geom.UHDynamic)
        points.addNextVertices(1)
        points.closePrimitive()

        geom = Geom(vdata)
        geom.addPrimitive(points)
        node = GeomNode("trail_particle")
        node.addGeom(geom)

        trail_particle_node = self.trail_node.attachNewNode(node)
        trail_particle_node.setPos(*self.position)
        trail_particle_node.setBin("fixed", 0)
        trail_particle_node.setDepthWrite(False)
        trail_particle_node.setRenderMode(RenderModeAttrib.MPoint, 5)

        return trail_particle_node

    def update(self, task):
        dt = globalClock.getDt()
        self.position = tuple(p + v * dt for p, v in zip(self.position, self.velocity))
        self.node.setPos(*self.position)

        self.update_trail()

        return Task.cont
        

    def update_trail(self):
        for particle in self.trail_particles:
            if particle['life'] <= 0:
                particle['node'].removeNode()

        self.trail_particles = [particle for particle in self.trail_particles if particle['life'] > 0]

        new_particle_node = self.create_trail_particle()
        new_particle = {
            'node': new_particle_node,
            'life': 1.0,  # full life span
            'decay': 0.01  # how quickly the particle fades
        }
        self.trail_particles.append(new_particle)

        for particle in self.trail_particles:
            particle['life'] -= particle['decay']
            particle['node'].setSa(particle['life'])

    
    def set_position(self, pos):
        self.position = pos
        self.node.setPos(*self.position)



class CometApp(ShowBase):
    def __init__(self):
        super().__init__()
        self.setBackgroundColor(0, 0, 0)

        self.comet = Comet()
        self.comet.node.reparentTo(self.render)
        self.taskMgr.add(self.update_comet, "update_comet")

        ambientLight = AmbientLight('ambientLight')
        ambientLight.setColor(Vec4(0.3, 0.3, 0.3, 1))
        ambientLightNP = self.render.attachNewNode(ambientLight)
        self.render.setLight(ambientLightNP)

        self.camera.setPos(0, 0, 0)
        self.camera.lookAt(self.comet.node)

    def update_comet(self, task):
        self.comet.update(task)
        return task.cont

if __name__ == '__main__':
    app = CometApp()
    app.run()