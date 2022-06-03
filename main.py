# modules
import pygame
import math

'''
Astronomical Measures used in calculations are:
AU - Astronomical Unit
G - Gravitational Constant
'''

# pygame window constants
WIDTH, HEIGHT = 800, 800
WHITE = (255, 255, 255)

# initialize pygame
pygame.init()

# pygame window constraints
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basic Planet Simulation")


class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11

    # required to down size astronomical parameters to our requirements
    SCALE = 250 / AU        # 1 AU = 100 pixels

    TIMESTEP = 3600 * 24    # 1 day

    def __init__(self, x, y, radius, color, mass):
        # x and y represents apogee and perigee distance of a planet from the sun
        self.x = x
        self.y = y

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
        x = self.x * self.SCALE + WIDTH/2 
        y = self.y * self.SCALE + HEIGHT/2

        pygame.draw.circle(win, self.color, (x, y), self.radius)


# Main Program
def main():
    run = True
    # Frame rate of animation
    clock = pygame.time.Clock()


    while run:
        # updates window 60 times per second
        clock.tick(60)

        # WIN.fill(WHITE)
        # pygame.display.update()

        # checks for events on pygame window
        for event in pygame.event.get():
            # checks if quit event is trigerred
            if event.type == pygame.QUIT:
                run = False     # breaking condition for 'while' loop

            
    # called after quit event is trigerred on pygame window
    pygame.quit()

# Call to Main Program
main()