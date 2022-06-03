# modules
import pygame
import math

'''
Astronomical Measures used in calculations are:
AU - Astronomical Unit
G - Gravitational Constant
'''

#  color constants
OFF_WHITE = (237,231,218)
VERMILLION = (215,56,6)
BLUE = (82,91,153)
RED = (236,124,90)
GREY = (126,123,126)
SIENNA = (193,145,86)
COBALT_BLUE = (119,150,190)
PEARL_BLUE = (210,248,251)
YELLOWISH_WHITE = (227,200,83)

# mass constants of planets (in kgs)
SUN_MASS = 1.98892 * 10**30
MERCURY_MASS = 3.301 * 10**23
VENUS_MASS = 4.8685 * 10**24
EARTH_MASS = 5.9742 * 10**24
MARS_MASS = 6.417 * 10**23
JUPITER_MASS = 1.899 * 10**27
SATURN_MASS = 5.685 * 10**26
URANUS_MASS = 8.682 * 10**25
NEPTUNE_MASS = 1.024 * 10**26

# initialize pygame
pygame.init()

# pygame window constants
WIDTH, HEIGHT = 800, 800

# pygame window attributes
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basic Planet Simulation")


class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11

    # required to down size astronomical parameters to our requirements
    SCALE = 200 / AU        # 1 AU = 100 pixels

    TIMESTEP = 3600 * 24    # 1 day is simulated per fps

    def __init__(self, x, y, radius, color, mass):
        # x and y represents apogee and perigee distance of a planet from the sun
        self.x = x
        self.y = y

        # properties of planets
        self.radius = radius
        self.color = color
        self.mass = mass

        # orbit list will be needed to record the co-ordinates of orbit a planet travels along
        self.orbit = []

        # Flag set to specify if planet is a sun or not
        self.sun = False

        self.distance_to_sun = 0

        # Parameters required for rotation velocity of planets
        # For sun, this remains 0
        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2 
        y = self.y * self.SCALE + HEIGHT / 2

        pygame.draw.circle(win, self.color, (x, y), self.radius)

# Create Planets
def getPlanets():
    # SUN
    sun = Planet(0, 0, 30, VERMILLION, SUN_MASS)
    sun.sun = True

    # MERCURY
    mercury = Planet(0.387 * Planet.AU, 0, 8, GREY, MERCURY_MASS)

    # VENUS
    venus = Planet(0.723 * Planet.AU, 0, 14, YELLOWISH_WHITE, VENUS_MASS)

    # EARTH
    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, EARTH_MASS)

    # MARS
    mars = Planet(-1.542 * Planet.AU, 0, 12, RED, MARS_MASS)

    # JUPITER
    # jupiter = Planet(-1 * Planet.AU, 0, 16, OFF_WHITE, JUPITER_MASS)

    # # SATURN
    # saturn = Planet(-1 * Planet.AU, 0, 16, SIENNA, SATURN_MASS)

    # # URANUS
    # uranus = Planet(-1 * Planet.AU, 0, 16, PEARL_BLUE, URANUS_MASS)

    # # NEPTUNE
    # neptune = Planet(-1 * Planet.AU, 0, 16, COBALT_BLUE, NEPTUNE_MASS)

    return [sun, mercury, venus, earth, mars]

# Main Program
def main():
    run = True
    # Frame rate of simulation
    clock = pygame.time.Clock()

    while run:
        # updates window 60 times per second
        clock.tick(60)

        # checks for events on pygame window
        for event in pygame.event.get():
            # checks if quit event is trigerred
            if event.type == pygame.QUIT:
                run = False     # breaking condition for 'while' loop

        #  list of planets in simulation
        planets = getPlanets()

        # draws planet specified in the 'planets' list
        for planet in planets:
            planet.draw(WIN)

        pygame.display.update()

    # called after quit event is trigerred on pygame window
    pygame.quit()

# Call to Main Program
main()