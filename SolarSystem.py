import numpy as np

from spacepy.spaceobjects import SpaceObject, StarSystem, State
from spacepy.constants import *
from astropy.time import Time
from astropy.coordinates import SkyCoord
from astroquery.jplhorizons import Horizons

def spaceobj_from_horizons(date, ID, name, mass, color):
    object_data = Horizons(id=ID, location="@sun", epochs=Time(date).tdb.jd).vectors(refplane='ecliptic')
    object_pos = SkyCoord(object_data['x'].quantity, object_data['y'].quantity, object_data['z'].quantity,
                          representation_type='cartesian', frame='heliocentriceclipticiau76', obstime=Time(date))
    object_vel = SkyCoord(object_data['vx'].quantity, object_data['vy'].quantity, object_data['vz'].quantity,
                          representation_type='cartesian', frame='heliocentriceclipticiau76', obstime=Time(date))
    return SpaceObject(name=name, mass=mass, initial_state=State(
                       position=np.array([object_pos.to_table().as_array()[0][0],
                                          object_pos.to_table().as_array()[0][1],
                                          object_pos.to_table().as_array()[0][2]]),
                       velocity=np.array([object_vel.to_table().as_array()[0][0],
                                          object_vel.to_table().as_array()[0][1],
                                          object_vel.to_table().as_array()[0][2]])), color=color)


# Planets definitions:
mercury = spaceobj_from_horizons("2022-01-12", 1, 'Mercury', MERCURY_MASS, MERCURY_COLOR)
venus = spaceobj_from_horizons("2022-01-12", 2, 'Venus', VENUS_MASS, VENUS_COLOR)
earth = spaceobj_from_horizons("2022-01-12", 3, 'Earth', EARTH_MASS, EARTH_COLOR)
mars = spaceobj_from_horizons("2022-01-12", 4, 'Mars', MARS_MASS, MARS_COLOR)
jupiter = spaceobj_from_horizons("2022-01-12", 5, 'Jupiter', JUPITER_MASS, JUPITER_COLOR)

# Solar system definition:
solar_system = StarSystem('Solar System', 'Sun', SUN_MASS, SUN_COLOR)
solar_system.add_planet(mercury)
solar_system.add_planet(venus)
solar_system.add_planet(earth)
solar_system.add_planet(mars)
solar_system.add_planet(jupiter)

# Simulating the system:
solar_system.simulate()


