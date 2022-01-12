import numpy as np
from enum import Enum
from spacepy.renderer import Render2D
from spacepy.constants import *

class RenderType(Enum):
    PLOT_2D = 0
    PLOT_3D = 1
    SCENE_3D = 2


class State:
    def __init__(self, position=np.zeros((3, 1)), velocity=np.zeros((3, 1)), acceleration=np.zeros((3, 1))):
        self.pos = position
        self.vel = velocity
        self.acc = acceleration


class SpaceObject:
    def __init__(self, name='Planet', mass=10e24, initial_state=State(), color='black'):
        self.name = name
        self.mass = mass
        self.prev_state = initial_state
        self.actual_state = initial_state
        self.color = color


class StarSystem:
    def __init__(self, star_system_name='Solar System', star_name='Sun', star_mass=SUN_MASS,
                 star_color=SUN_COLOR, render_type=RenderType.PLOT_2D):
        # Star (SpaceObject):
        self.star = SpaceObject(name=star_name, mass=star_mass, color=star_color)

        # List of planets:
        self.planets = []

        # Renderer:
        if render_type == RenderType.PLOT_2D:
            self.render = Render2D(star_system_name)

    def add_planet(self, planet=SpaceObject('Planet', 10 ** 6, State(), '#ffffff')):
        self.planets.append(planet)

    def simulate(self):
        self.render.display(self.star, self.planets)
