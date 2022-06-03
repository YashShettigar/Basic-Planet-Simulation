# modules
import pygame
import math

'''
Astronomical Measures used in calculations are:
AU - Astronomical Unit
G - Gravitational Constant
'''

#  COLOR CONSTANTS
OFF_WHITE = (237,231,218)
VERMILLION = (215,56,6)
BLUE = (82,91,153)
RED = (236,124,90)
GREY = (126,123,126)
SIENNA = (193,145,86)
COBALT_BLUE = (119,150,190)
PEARL_BLUE = (210,248,251)
YELLOWISH_WHITE = (227,200,83)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# MASS CONSTANTS OF PLANETS (in kgs)
SUN_MASS = 1.98892 * 10**30
MERCURY_MASS = 3.301 * 10**23
VENUS_MASS = 4.8685 * 10**24
EARTH_MASS = 5.9742 * 10**24
MARS_MASS = 6.417 * 10**23
JUPITER_MASS = 1.899 * 10**27
SATURN_MASS = 5.685 * 10**26
URANUS_MASS = 8.682 * 10**25
NEPTUNE_MASS = 1.024 * 10**26

# VELOCITY CONSTANTS FOR PLANETS
Y_VEL_MERCURY = 47.36 * 1000
Y_VEL_VENUS = 35.02 * 1000
Y_VEL_EARTH = 29.78 * 1000
Y_VEL_MARS = 24.07 * 1000
Y_VEL_JUPITER = 13.06 * 1000
Y_VEL_SATURN = 9.68 * 1000
Y_VEL_URANUS = 6.80 * 1000
Y_VEL_NEPTUNE = 5.43 * 1000

# initialize pygame window
pygame.init()

# pygame window attributes
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basic Planet Simulation")

FONT = pygame.font.SysFont("comicsans", 14)

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11

    # required to down size astronomical parameters to our requirements
    SCALE = 250 / AU        # 1 AU = 100 pixels

    TIMESTEP = 3600 * 24    # 1 day is simulated per fps

    def __init__(self, x, y, radius, color, mass):
        # x and y represents x-intercept and y-intercept distance of a planet from the sun
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


        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (x, y), self.radius)
        
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 2)}km", 1, WHITE)
            win.blit(distance_text, (x-distance_text.get_width()/2, y-distance_text.get_height()/2))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


# Create Planets
def getPlanets():
    # SUN
    sun = Planet(0, 0, 30, VERMILLION, SUN_MASS)
    sun.sun = True

    # MERCURY
    mercury = Planet(0.387 * Planet.AU, 0, 8, GREY, MERCURY_MASS)
    mercury.y_vel = -Y_VEL_MERCURY

    # VENUS
    venus = Planet(0.723 * Planet.AU, 0, 14, YELLOWISH_WHITE, VENUS_MASS)
    venus.y_vel = -Y_VEL_VENUS

    # EARTH
    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, EARTH_MASS)
    earth.y_vel = Y_VEL_EARTH

    # MARS
    mars = Planet(-1.542 * Planet.AU, 0, 12, RED, MARS_MASS)
    mars.y_vel = Y_VEL_MARS

    # # JUPITER
    # jupiter = Planet(-1 * Planet.AU, 0, 16, OFF_WHITE, JUPITER_MASS)
    # jupiter.y_vel = Y_VEL_JUPITER

    # # SATURN
    # saturn = Planet(-1 * Planet.AU, 0, 16, SIENNA, SATURN_MASS)
    # saturn.y_vel = Y_VEL_SATURN

    # # URANUS
    # uranus = Planet(-1 * Planet.AU, 0, 16, PEARL_BLUE, URANUS_MASS)
    # uranus.y_vel = Y_VEL_URANUS

    # # NEPTUNE
    # neptune = Planet(-1 * Planet.AU, 0, 16, COBALT_BLUE, NEPTUNE_MASS)
    # neptune.y_vel = Y_VEL_NEPTUNE

    return [sun, mercury, venus, earth, mars]

# Main Program
def main():
    run = True
    # Frame rate of simulation
    clock = pygame.time.Clock()

    #  list of planets in simulation
    planets = getPlanets()

    while run:
        # updates window 60 times per second
        clock.tick(60)
        WIN.fill(BLACK)

        # checks for events on pygame window
        for event in pygame.event.get():
            # checks if quit event is trigerred
            if event.type == pygame.QUIT:
                run = False     # breaking condition for 'while' loop

        # draws planet specified in the 'planets' list
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    # called after quit event is trigerred on pygame window
    pygame.quit()

# Call to Main Program
main()