from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties, Vec3
from direct.task import Task
import sys
import random
import math

from Comet import Comet
from Nebula import Nebula
from Planet import Planet
from Star import Star


class SpaceScene(ShowBase):

    def __init__(self):
        super().__init__()

        self.procedural_objects = []

        self.disableMouse()

        properties = WindowProperties()
        properties.setCursorHidden(True)
        properties.setMouseMode(WindowProperties.M_confined)
        self.win.requestProperties(properties)

        w, h = 1664, 936

        props = WindowProperties() 
        props.setSize(w, h) 

        self.win.requestProperties(props)

        self.camera.setPos(0, 0, 0)
        self.camera.setHpr(0, 0, 0)

        self.movement_speed = 50
        self.mouse_sensitivity = 0.1
        self.win.movePointer(0, self.win.getXSize() // 2, self.win.getYSize() // 2)
        
        self.key_map = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False,
            "up": False,
            "down": False
        }

        self.accept("w", self.update_key_map, ["forward", True])
        self.accept("w-up", self.update_key_map, ["forward", False])
        self.accept("s", self.update_key_map, ["backward", True])
        self.accept("s-up", self.update_key_map, ["backward", False])
        self.accept("a", self.update_key_map, ["left", True])
        self.accept("a-up", self.update_key_map, ["left", False])
        self.accept("d", self.update_key_map, ["right", True])
        self.accept("d-up", self.update_key_map, ["right", False])
        self.accept("space", self.update_key_map, ["up", True])
        self.accept("space-up", self.update_key_map, ["up", False])
        self.accept("shift", self.update_key_map, ["down", True])
        self.accept("shift-up", self.update_key_map, ["down", False])
        self.accept("escape", sys.exit)

        self.taskMgr.add(self.move, "moveTask")
        self.taskMgr.add(self.mouse_look, "mouseLookTask")

        self.setup_scene()

        self.taskMgr.add(self.procedural_generation, "procedural_generation")

    def update_key_map(self, control_name, is_down):
        self.key_map[control_name] = is_down


    def procedural_generation(self, task):
        if self.should_add_object():
            object_type = random.choice(['comet', 'nebula', 'planet', 'star'])
            position = self.random_position_around_camera(distance=500)
            
            if object_type == 'comet':
                comet = Comet(radius=random.uniform(4, 15), pos=position, velocity=(random.uniform(1, 5.0), 0, random.uniform(1, 5.0)))
                comet.node.reparentTo(self.render)
                self.procedural_objects.append(comet)
            
            elif object_type == 'nebula':
                nebula = Nebula(scale=random.uniform(0.5, 4.0), pos=position,
                                num_arms=random.randint(2, 5), points_per_arm=random.randint(200, 2000),
                                thickness=random.uniform(0.1, 1))
                nebula.node.reparentTo(self.render)
                self.procedural_objects.append(nebula)
            
            elif object_type == 'planet':
                planet = Planet(radius=random.uniform(100.0, 5.0), pos=position,
                                 has_rings=random.random() < 0.2, ring_color=(1, 0.9, 0.8, 0.3))
                planet.node.reparentTo(self.render)
                self.procedural_objects.append(planet)
            
            elif object_type == 'star':
                star = Star(radius=random.uniform(0.5, 1.5), pos=position)
                star.node.reparentTo(self.render)
                self.procedural_objects.append(star)
        
        return task.cont

    def move(self, task):
        dt = globalClock.getDt()
        if self.key_map["forward"]:
            self.camera.setY(self.camera, self.movement_speed * dt)
        if self.key_map["backward"]:
            self.camera.setY(self.camera, -self.movement_speed * dt)
        if self.key_map["left"]:
            self.camera.setX(self.camera, -self.movement_speed * dt)
        if self.key_map["right"]:
            self.camera.setX(self.camera, self.movement_speed * dt)
        if self.key_map["up"]:
            self.camera.setZ(self.camera, self.movement_speed * dt)
        if self.key_map["down"]:
            self.camera.setZ(self.camera, -self.movement_speed * dt)
        return Task.cont

    def mouse_look(self, task):
        md = self.win.getPointer(0)
        x = md.getX()
        y = md.getY()
        if self.win.movePointer(0, int(self.win.getXSize() / 2), int(self.win.getYSize() / 2)):
            self.camera.setH(self.camera.getH() - (x - self.win.getXSize() // 2) * self.mouse_sensitivity)
            self.camera.setP(self.camera.getP() - (y - self.win.getYSize() // 2) * self.mouse_sensitivity)
        return Task.cont

    def should_add_object(self):
        # Logic to decide if a new object should be added
        # This could be based on time, distance traveled, or number of objects currently in the scene
        return random.random() < 0.04


    def random_position_around_camera(self, distance):
        # Generate a random position around the camera within the given distance
        angle = random.uniform(0, 2 * math.pi)
        x = self.camera.getX() + distance * math.cos(angle)
        y = self.camera.getY() + distance * math.sin(angle)
        z = random.uniform(-distance / 2, distance / 2)  # some variation in the z-axis
        return (x, y, z)

    def random_velocity(self):
        # Generate a random velocity vector
        return (random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1))


    def setup_scene(self):
        # Procedurally generate the space scene
        for _ in range(5):
            x, y, z = [random.uniform(-100, 100) for _ in range(3)]
            planet = Planet(random.uniform(0.5, 2.5), pos=(x, y, z))
            planet.node.reparentTo(self.render)

        # Generate some stars
        for _ in range(20):  # Generate 20 random stars
            x, y, z = [random.uniform(-100, 100) for _ in range(3)]
            star = Star(pos=(x, y, z))
            star.node.reparentTo(self.render)

        # Generate a comet
        comet = Comet(radius=0.1, pos=(10, 20, -10), velocity=(-0.05, 0, 0))
        comet.node.reparentTo(self.render)

        # Generate a nebula
        nebula = Nebula(scale=5, pos=(0, 0, 0), num_arms=3, points_per_arm=100, thickness=0.5)
        nebula.node.reparentTo(self.render)

    


if __name__ == "__main__":
    app = SpaceScene()
    app.run()
