from panda3d.core import (NodePath, GeomNode, Geom, GeomVertexFormat, GeomVertexData,
                          GeomVertexWriter, GeomLines, Vec4, Material, AmbientLight,
                          RenderModeAttrib, TransparencyAttrib, ColorBlendAttrib, GeomPoints,
                          )
from direct.showbase.ShowBase import ShowBase
from direct.filter.CommonFilters import CommonFilters
import random
import numpy as np

class Nebula:

    def __init__(self, scale=1.0, pos=(0, 0, 0), num_arms=2, points_per_arm=100, thickness=0.1,
                  num_particles=10, point_size=8, depth=5.0):
        self.scale = scale
        self.position = pos
        self.num_arms = num_arms
        self.points_per_arm = points_per_arm
        self.thickness = thickness
        self.num_particles = num_particles
        self.point_size = point_size
        self.depth = depth
        self.node = self.create_nebula()

        self.node.setP(-90) # pitch rotation to make the nebula face the camera

    def create_nebula(self):
        format = GeomVertexFormat.getV3n3cpt2()
        vdata = GeomVertexData('nebula', format, Geom.UHDynamic)
        
        vertex = GeomVertexWriter(vdata, 'vertex')
        normal = GeomVertexWriter(vdata, 'normal')
        color_writer = GeomVertexWriter(vdata, 'color')  # Renamed to avoid conflict
        texcoord = GeomVertexWriter(vdata, 'texcoord')

        # Generate points for the spiral arms and the surrounding particles --
        # uses the formula r = scale * theta, where theta is the angle around the arm
        for arm in range(self.num_arms):
            angle_offset = 2 * np.pi * arm / self.num_arms
            for i in range(self.points_per_arm):
                theta = i / (self.points_per_arm - 1) * 2 * np.pi + angle_offset
                r = self.scale * theta
                x = r * np.cos(theta)
                y = r * np.sin(theta)
                z = 0 

                # Create points around the arm points to simulate the nebula cloud
                for p in range(self.num_particles):  # per point on each arm

                    # Randomize the position around the arm point to give a cloud-like appearance
                    px = x + random.uniform(-self.thickness, self.thickness)
                    py = y + random.uniform(-self.thickness, self.thickness)
                    pz = z + random.uniform(-self.thickness * self.depth, self.thickness * self.depth)
                    vertex.addData3f(px, py, pz)
                    normal.addData3f(0, 0, 1)

                    factor = i / (self.points_per_arm - 1)
                    neb_color = self.generate_random_nebula_color(factor)
                    color_writer.addData4f(neb_color[0], neb_color[1], neb_color[2], 1.0)  # Full opacity for now
                    texcoord.addData2f(factor, arm / self.num_arms)

        # Use GeomPoints for rendering the nebula
        points = GeomPoints(Geom.UHDynamic)
        points.addNextVertices(self.num_arms * self.points_per_arm * self.num_particles)
        points.closePrimitive()
        geom = Geom(vdata)
        geom.addPrimitive(points)

        node = GeomNode('nebula')
        node.addGeom(geom)
        nebula_node = NodePath(node)
        nebula_node.setPos(*self.position)

        # Material and render attributes -- matte
        nebula_material = Material()
        nebula_material.setEmission(Vec4(0.2, 0.2, 0.8, 1))  # blue-ish glow
        nebula_node.setMaterial(nebula_material)
        
        # Set render mode for points and enable additive blending
        nebula_node.setRenderMode(RenderModeAttrib.MPoint, self.point_size)  # Point size
        nebula_node.setTransparency(TransparencyAttrib.MAlpha)
        nebula_node.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))
        nebula_node.setDepthWrite(True)

        return nebula_node


    def generate_random_nebula_color(self, factor):
        """
        Generate a color gradient for the nebula based on the factor (ranging from 0 to 1).
        """
        # Define the start and end colors for the gradient
        start_color = np.array([0.5, 0.0, 0.5, 1.0])  # Purple
        end_color = np.array([0.0, 0.0, 1.0, 1.0])    # Blue

        color = (1 - factor) * start_color + factor * end_color
        return tuple(color)



class NebulaApp(ShowBase):

    def __init__(self):
        super().__init__()

        # Set a darker background to contrast with the nebula
        base.setBackgroundColor(0, 0, 0)
        self.nebula_instance = Nebula(scale=0.3, num_arms=5, points_per_arm=1000, thickness=0.7)
        nebula_node = self.nebula_instance.node
        nebula_node.reparentTo(self.render)

        ambient_light = AmbientLight('ambient')
        ambient_light.setColor((0.2, 0.2, 0.2, 1))
        ambient_light_np = self.render.attachNewNode(ambient_light)
        self.render.setLight(ambient_light_np)
        self.camera.setPos(0, 0, 0)



if __name__ == '__main__':
    app = NebulaApp()
    app.run()
    