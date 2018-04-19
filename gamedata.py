WIDTH = 1024  # Width of game area.
HEIGHT = 384  # Height of game area.
speed = 20  # How fast non-player objects move.
object_frequency = 100  # Smaller = more frequent.
steps = 0  # Counts the number of frames so far in the game.
PULL = 3  # Cost of kicking
PUSH = 3  # Benefit of flying
FALL = 5  # Cost of hitting somthing.
FLIGHT_TIME = 2  # Number of seconds flying.
END = False  # Has the game finished..?

objects = {
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