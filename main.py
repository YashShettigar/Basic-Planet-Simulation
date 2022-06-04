# modules
import pygame
import math

SUN_IMG = pygame.image.load('planet-images/sun.jpg')
MERCURY_IMG = pygame.image.load('planet-images/mercury.png')
VENUS_ING = pygame.image.load('planet-images/venus.png')
EARTH_IMG = pygame.image.load('planet-images/earth.png')
MARS_IMG = pygame.image.load('planet-images/mars.png')
JUPITER_IMG = pygame.image.load('planet-images/jupiter.png')
SATURN_IMG = pygame.image.load('planet-images/saturn.jpg')
URANUS_IMG = pygame.image.load('planet-images/uranus.png')
NEPTUNE_IMG = pygame.image.load('planet-images/neptune.png')

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

# MEAN RADIAL CONSTANTS FOR PLANETS
SUN_RADIUS = 695700 * 1000
MERCURY_RADIUS = 2439.7 * 1000
VENUS_RADIUS = 6051.8 * 1000
EARTH_RADIUS = 6371 * 1000
MARS_RADIUS = 3389.5 * 1000
JUPITER_RADIUS = 69911 * 1000
SATURN_RADIUS = 58232 * 1000
URANUS_RADIUS = 25362 * 1000
NEPTUNE_RADIUS = 24622 * 1000

# ORBITAL DISTANCE OF PLANETS
OD_SUN = 0
OD_MERCURY = 0.387
OD_VENUS = 0.723
OD_EARTH = 1
OD_MARS = 1.542
OD_JUPITER = 5.204
OD_SATURN = 9.582
OD_URANUS = 19.23
OD_NEPTUNE = 30.10

# initialize pygame window
pygame.init()

# pygame window attributes
WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basic Planet Simulation")

FONT = pygame.font.SysFont("comicsans", 14)

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11

    # required to down size astronomical parameters to our requirements
    SCALE = 150 / AU        # 1 AU = 100 pixels

    TIMESTEP = 3600 * 24    # 1 day is simulated per fps

    def __init__(self, x, y, radius, color, mass, img, img_size):
        # x and y represents x-intercept and y-intercept distance of a planet from the sun
        self.x = x
        self.y = y

        # properties of planets
        self.radius = radius
        self.color = color
        self.mass = mass

        self.img = img
        
        # img properties
        self.img_size = img_size

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

            pygame.draw.lines(win, WHITE, False, updated_points, 1)

        win.blit(pygame.transform.scale(self.img, self.img_size), (x - self.img_size[0]/2, y - self.img_size[1]/2))
        # pygame.draw.circle(win, self.color, (x, y), self.radius)

        # if not self.sun:
        #     distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 2)}km", 1, WHITE)
        #     win.blit(distance_text, (x-distance_text.get_width()/2, y-distance_text.get_height()/2))

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
    sun = Planet(OD_SUN * Planet.AU, 0, 30, VERMILLION, SUN_MASS, SUN_IMG, (40, 40))
    sun.sun = True

    # MERCURY
    mercury = Planet(OD_MERCURY * Planet.AU, 0, 8, GREY, MERCURY_MASS, MERCURY_IMG, (20, 20))
    mercury.y_vel = -Y_VEL_MERCURY

    # VENUS
    venus = Planet(OD_VENUS * Planet.AU, 0, 14, YELLOWISH_WHITE, VENUS_MASS, VENUS_ING, (20, 20))
    venus.y_vel = -Y_VEL_VENUS

    # EARTH
    earth = Planet(-OD_EARTH * Planet.AU, 0, 16, BLUE, EARTH_MASS, EARTH_IMG, (20, 20))
    earth.y_vel = Y_VEL_EARTH

    # MARS
    mars = Planet(-OD_MARS * Planet.AU, 0, 12, RED, MARS_MASS, MARS_IMG, (20, 20))
    mars.y_vel = Y_VEL_MARS

    # JUPITER
    jupiter = Planet(OD_JUPITER * Planet.AU, 0, 16, OFF_WHITE, JUPITER_MASS, JUPITER_IMG, (20, 20))
    jupiter.y_vel = Y_VEL_JUPITER

    # SATURN
    saturn = Planet(OD_SATURN * Planet.AU, 0, 16, SIENNA, SATURN_MASS, SATURN_IMG, (20, 20))
    saturn.y_vel = Y_VEL_SATURN

    # URANUS
    uranus = Planet(-OD_URANUS * Planet.AU, 0, 16, PEARL_BLUE, URANUS_MASS, URANUS_IMG, (20, 20))
    uranus.y_vel = Y_VEL_URANUS

    # NEPTUNE
    neptune = Planet(-OD_NEPTUNE * Planet.AU, 0, 16, COBALT_BLUE, NEPTUNE_MASS, NEPTUNE_IMG, (20, 20))
    neptune.y_vel = Y_VEL_NEPTUNE

    return [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

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