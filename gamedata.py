"""
Contains definitions of the various assets used in the
game.
"""

from pgzero.actor import Actor

WIDTH = 1024  # Width of game area.
HEIGHT = 384  # Height of game area.
DISTANCE = 200  # The distance to win by.
LEVEL_UP = 100  # Number of steps before making more difficult.
speed = 20  # How fast non-player objects move.
object_frequency = 100  # Smaller = more frequent.
powerup_frequency = 400  # How likely a powerup will appear.
steps = 0  # Counts the number of frames so far in the game.
PULL = 2  # Cost of kicking
PUSH = 2  # Benefit of flying
FALL = 10  # Cost of hitting somthing.
FLIGHT_TIME = 2  # Number of seconds flying.
STARTED = False  # Has the race started..?
END = False  # Has the game finished..?
WARNING = False  # Flash the distance warning.

ground_objects = {
    'small_ground': {
        'pos': [320, 320],
        'items': [
            'cat',
            'dog',
            'box',
            'fire_hydrant',
            'traffic_cone',
            'undergrowth',
        ],
    },
    'large_ground': {
        'pos': [312, 312],
        'items': [
            'barrels',
            'barrier',
            'bushes',
            'fence', 
            'motorbike',
        ],
    },
}

air_objects = {
    'small_air': {
        'pos': [48, 280],
        'items': [
            'kite',
            'star',
        ],
    },
    'large_air': {
        'pos': [64, 240],
        'items': [
            'balloon',
            'comet',
            'cloud',
            'jet',
            'satellite',
        ],
    },
}

active_objects = []  # Non-player objects to avoid.
power_up = None  # Represents am antigravity power-up in the game world.


red = Actor('red_run1')  # Represents "Red"
red.name = 'red'  # Used to select which colour animation to use.
red.pos = (512, 304)  # Start position
red.frame = 1  # Start frame for the animations.
red.jumping = False  # Jumping state.
red.flying = False  # Flying state.
red.kicking = False  # Kicking state.
red.landing = False  # Landing state.
red.hit = False  # Hit non-player object state.
red.antigravity = 0  # The number of "flights" red can make.

blue = Actor('blue_run1')  # Represents "Blue"
blue.name = 'blue'  # Used to select which colour animation to use.
blue.pos = (512, 304)  # Start position.
blue.frame = 3  # Start frame for the animation.
blue.jumping = False  # Jumping state.
blue.flying = False  # Flying state.
blue.kicking = False  # Kicking state.
blue.landing = False  # Landing state.
blue.hit = False  # Hit non-player object state.
blue.antigravity = 0  # The number of "flights" blue can make.

# Floors are drawn one after the other for smooth scrolling.
floor_a = Actor('floor')
floor_a.pos = 0, 332
floor_b = Actor('floor')
floor_b.pos = 1024, 332