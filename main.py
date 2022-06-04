# modules
import pygame
import math

# load planet images
SUN_IMG = pygame.image.load('planet-images/sun.jpg')
MERCURY_IMG = pygame.image.load('planet-images/mercury.png')
VENUS_ING = pygame.image.load('planet-images/venus.png')
EARTH_IMG = pygame.image.load('planet-images/earth.png')
MARS_IMG = pygame.image.load('planet-images/mars.png')
JUPITER_IMG = pygame.image.load('planet-images/jupiter.png')
SATURN_IMG = pygame.image.load('planet-images/saturn.jpg')
URANUS_IMG = pygame.image.load('planet-images/uranus.png')
NEPTUNE_IMG = pygame.image.load('planet-images/neptune.png')

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

# VELOCITY CONSTANTS OF PLANETS
Y_VEL_MERCURY = 47.36 * 1000
Y_VEL_VENUS = 35.02 * 1000
Y_VEL_EARTH = 29.78 * 1000
Y_VEL_MARS = 24.07 * 1000
Y_VEL_JUPITER = 13.06 * 1000
Y_VEL_SATURN = 9.68 * 1000
Y_VEL_URANUS = 6.80 * 1000
Y_VEL_NEPTUNE = 5.43 * 1000

# MEAN VOLUMETRIC RADIAL CONSTANTS OF PLANETS
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

FONT = pygame.font.SysFont("timesnewroman", 30, True)

'''
Astronomical Measures used in calculations are:
AU - Astronomical Unit
G - Gravitational Constant
'''

AU = 149.6e6 * 1000
G = 6.67428e-11

TIMESTEP = 3600 * 24    # 1 day is simulated per fps

class Planet:
    def __init__(self, x, y, radius, color, mass, img, img_size,):
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

    def draw(self, win, scale):
        x = self.x * scale + WIDTH / 2 
        y = self.y * scale + HEIGHT / 2


        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * scale + WIDTH / 2
                y = y * scale + HEIGHT / 2
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

        force = G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            # to avoid zero division error
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * TIMESTEP
        self.y_vel += total_fy / self.mass * TIMESTEP

        self.x += self.x_vel * TIMESTEP
        self.y += self.y_vel * TIMESTEP
        self.orbit.append((self.x, self.y))


# Create Planets
def getPlanets():
    # SUN
    sun = Planet(OD_SUN * AU, 0, SUN_RADIUS, VERMILLION, SUN_MASS, SUN_IMG, (40, 40))
    sun.sun = True

    # MERCURY
    mercury = Planet(OD_MERCURY * AU, 0, MERCURY_RADIUS, GREY, MERCURY_MASS, MERCURY_IMG, (20, 20))
    mercury.y_vel = -Y_VEL_MERCURY

    # VENUS
    venus = Planet(OD_VENUS * AU, 0, VENUS_RADIUS, YELLOWISH_WHITE, VENUS_MASS, VENUS_ING, (20, 20))
    venus.y_vel = -Y_VEL_VENUS

    # EARTH
    earth = Planet(-OD_EARTH * AU, 0, EARTH_RADIUS, BLUE, EARTH_MASS, EARTH_IMG, (20, 20))
    earth.y_vel = Y_VEL_EARTH

    # MARS
    mars = Planet(-OD_MARS * AU, 0, MARS_RADIUS, RED, MARS_MASS, MARS_IMG, (20, 20))
    mars.y_vel = Y_VEL_MARS

    # JUPITER
    jupiter = Planet(OD_JUPITER * AU, 0, JUPITER_RADIUS, OFF_WHITE, JUPITER_MASS, JUPITER_IMG, (20, 20))
    jupiter.y_vel = Y_VEL_JUPITER

    # SATURN
    saturn = Planet(OD_SATURN * AU, 0, SATURN_RADIUS, SIENNA, SATURN_MASS, SATURN_IMG, (20, 20))
    saturn.y_vel = Y_VEL_SATURN

    # URANUS
    uranus = Planet(-OD_URANUS * AU, 0, URANUS_RADIUS, PEARL_BLUE, URANUS_MASS, URANUS_IMG, (20, 20))
    uranus.y_vel = Y_VEL_URANUS

    # NEPTUNE
    neptune = Planet(-OD_NEPTUNE * AU, 0, NEPTUNE_RADIUS, COBALT_BLUE, NEPTUNE_MASS, NEPTUNE_IMG, (20, 20))
    neptune.y_vel = Y_VEL_NEPTUNE

    return [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]


# add zoom buttons to the window
def addZoomButtons(BTN_WIDTH, BTN_HEIGHT, ZOOM_IN_BTN_X, ZOOM_OUT_BTN_X, BTN_Y):
    # for zoom in
    zoomInText = FONT.render('+', 1, WHITE)
    pygame.draw.rect(WIN, WHITE, [ZOOM_IN_BTN_X, BTN_Y, BTN_WIDTH, BTN_HEIGHT], 2, 0, 8, 0, 8, 0)
    WIN.blit(zoomInText, (ZOOM_IN_BTN_X - zoomInText.get_width()/2 + BTN_WIDTH/2, BTN_Y + BTN_HEIGHT/2 - zoomInText.get_height()/2))

    # for zoom out
    zoomOutText = FONT.render('-', 1, WHITE)
    pygame.draw.rect(WIN, WHITE, [ZOOM_OUT_BTN_X, BTN_Y, BTN_WIDTH, BTN_HEIGHT], 2, 0, 0, 8, 0, 8)
    WIN.blit(zoomOutText, (ZOOM_OUT_BTN_X - zoomOutText.get_width()/2 + BTN_WIDTH/2, BTN_Y + BTN_HEIGHT/2 - zoomOutText.get_height()/2))


# Main Program
def main():
    run = True
    
    # Frame rate of simulation
    clock = pygame.time.Clock()

    # variable required to down size astronomical parameters to our window requirements
    scale = 150 / AU

    zoom = 0    # declared for keeping track of zoom scales

    #  list of planets in simulation
    planets = getPlanets()

    # add zoom in and zoom out buttons to the window
    BTN_WIDTH = 100
    BTN_HEIGHT = 40

    ZOOM_IN_BTN_X = WIDTH/2 - BTN_WIDTH
    ZOOM_OUT_BTN_X = WIDTH/2
    BTN_Y = HEIGHT - 2*BTN_HEIGHT - 10

    while run:
        # updates window 60 times per second
        clock.tick(60)
        WIN.fill(BLACK)

        addZoomButtons(BTN_WIDTH, BTN_HEIGHT, ZOOM_IN_BTN_X, ZOOM_OUT_BTN_X, BTN_Y)

        # checks for events on pygame window
        for event in pygame.event.get():
            # checks if quit event is trigerred
            if event.type == pygame.QUIT:
                run = False     # breaking condition for 'while' loop
            
            # checks for zoom in and zoom out of the window
            if event.type == pygame.MOUSEWHEEL:
                if event.y == -1:
                    if zoom != 3:
                        zoom += 1
                        scale *= 2
                else:
                    if zoom != -3:
                        zoom -= 1
                        scale /= 2
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # checks if mouse co-ordinates are within the range of y co-ordinates of button (height)
                if not (BTN_Y < mouseY) and (BTN_Y + BTN_HEIGHT > mouseY):
                    break

                # checks if mouse co-ordinates are within the range of x co-ordinates of ZOOM IN button (width)
                if (ZOOM_IN_BTN_X < mouseX) and (ZOOM_IN_BTN_X + BTN_WIDTH > mouseX):
                    if zoom != 3:
                        zoom += 1
                        scale *= 2
                # checks if mouse co-ordinates are within the range of x co-ordinates of ZOOM OUT button (width)
                elif (ZOOM_OUT_BTN_X < mouseX) and (ZOOM_OUT_BTN_X + BTN_WIDTH > mouseX):
                    if zoom != -3:
                        zoom -= 1
                        scale /= 2
                else:
                    break

        # draws planet specified in the 'planets' list
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN, scale)

        mouseX, mouseY = pygame.mouse.get_pos()

        pygame.display.update()

    # called after quit event is trigerred on pygame window
    pygame.quit()

# Call to Main Program
main()