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
        self.actual_state = State()
        self.color = color


class StarSystem:
    def __init__(self, star_system_name='Solar System', star_name='Sun', star_mass=SUN_MASS,
                 star_color=SUN_COLOR, render_type=RenderType.PLOT_2D):
        # Star (SpaceObject):
        self.star = SpaceObject(name=star_name, mass=star_mass, color=star_color)

        # List of planets:
        self.planets = []

        # List of states of the simulation:
        self.states = []

        # Renderer:
        if render_type == RenderType.PLOT_2D:
            self.render = Render2D(star_system_name, self.star)

    def add_planet(self, planet=SpaceObject('Planet', 10 ** 6, State(), '#ffffff')):
        self.planets.append(planet)

    def simulate(self, initial_day, number_of_days):
        dt = 1.0    # [day]
        for ii in range(0, number_of_days):
            tmp_states = []

            # Update position of all planets:
            for actual_planet in self.planets:
                actual_planet.actual_state.pos = actual_planet.prev_state.pos + actual_planet.prev_state.vel * dt
                print(f'Day: {ii}, Planet: {actual_planet.name}, PrevX = {actual_planet.prev_state.pos[0]}, ActualX = {actual_planet.actual_state.pos[0]}')
            # Computing new state:
            for actual_planet in self.planets:
                # Computing overall acceleration:
                actual_planet.actual_state.acc = - G_AU * self.star.mass * actual_planet.actual_state.pos / (
                    np.linalg.norm(actual_planet.actual_state.pos) ** 3)
                for other_planet in self.planets:
                    if other_planet.name != actual_planet.name:
                        distance_vector = other_planet.actual_state.pos - actual_planet.actual_state.pos
                        actual_planet.actual_state.acc += G_AU * other_planet.mass * distance_vector / (
                                np.linalg.norm(distance_vector) ** 3)
                # Computing new velocity:
                actual_planet.actual_state.vel = actual_planet.prev_state.vel + actual_planet.actual_state.acc * dt

                # Saving state:
                tmp_states.append(State(actual_planet.actual_state.pos, actual_planet.actual_state.vel,
                                        actual_planet.actual_state.acc))

                # Update values:
                actual_planet.prev_state.pos = actual_planet.actual_state.pos
                actual_planet.prev_state.vel = actual_planet.actual_state.vel
                actual_planet.prev_state.acc = actual_planet.actual_state.acc
            # Saving states timestamp:
            self.states.append(tmp_states[:])

        self.render.display(self.star, self.planets, self.states, initial_day, number_of_days)
