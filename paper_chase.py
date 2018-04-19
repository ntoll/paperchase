"""
Paper Chase.
"""
import random
from gamedata import *

red = Actor('red_run1')  # Represents "Red"
red.name = 'red'  # Used to select which colour animation to use.
red.pos = (256, 304)  # Start position
red.frame = 1  # Start frame for the animations.
red.jumping = False  # Jumping state.
red.flying = False  # Flying state.
red.kicking = False  # Kicking state.
red.hit = False  # Hit non-player object state.
red.antigravity = 0  # The number of "flights" red can make.

blue = Actor('blue_run1')  # Represents "Blue"
blue.name = 'blue'  # Used to select which colour animation to use.
blue.pos = (256, 304)  # Start position.
blue.frame = 3  # Start frame for the animation.
blue.jumping = False  # Jumping state.
blue.flying = False  # Flying state.
blue.kicking = False  # Kicking state.
blue.hit = False  # Hit non-player object state.
blue.antigravity = 0  # The number of "flights" blue can make.

# Floors are drawn one after the other for smooth scrolling.
floor_a = Actor('floor')
floor_a.pos = 0, 332
floor_b = Actor('floor')
floor_b.pos = 1024, 332

def update_player(player):
    """
    Given a player, will ensure the correct image is used
    for their current state.
    """
    if player.jumping:
        player.image = "{}_run3".format(player.name)
    elif player.kicking:
        player.image = "{}_kick".format(player.name)
        player.left -= PULL
    else:
        if player.flying:
            player.left += PUSH
            player.image = "{}_fly{}".format(player.name, player.frame)
        else:
            player.image = "{}_run{}".format(player.name, player.frame)
        player.frame += 1
        if player.frame > 5:
            player.frame = 1


def animate_update():
    """
    Update images so we have around 12 FPS.
    """
    global steps
    global speed
    global object_frequency
    global active_objects
    # Increase difficulty every 200 steps.
    steps += 1
    if steps % 200 == 0:
        speed = min(40, speed + 4)  # Non plays move faster.
        # Objects appear more frequently.
        object_frequency = max(50, object_frequency - 5)
    # Update player images.
    update_player(red)
    update_player(blue)
    # Scroll the floor continuously.
    floor_a.left -= speed
    floor_b.left -= speed
    if int(floor_a.right) < 0:
        floor_a.left = floor_b.right
    if int(floor_b.right) < 0:
        floor_b.left = floor_a.right
    # Move non-player objects.
    for obj in active_objects:
        obj.left -= speed
    # Check for winning condition
    distance_between_players = abs(red.left - blue.left)
    if (distance_between_players > 600 or red.right < 0 or 
            blue.right < 0):
        endgame()
    else:
        # Re-schedule a call to this function.
        clock.schedule_unique(animate_update, 0.08)
        
def endgame():
    END = True
    

def jump(player, on_finished):
    if not player.flying:
        player.jumping = True
        x, y = player.pos
        animate(player, pos=(x, 204), duration=0.5,
                on_finished=on_finished, tween='decelerate')

def fall(player, on_finished):
    x, y = player.pos
    animate(player, pos=(x, 304), duration=0.3, 
            on_finished=on_finished, tween='accelerate')

def fly_up(player):
    x, y = player.pos
    animate(player, pos=(x, max(20, y - 50)), 
            duration=0.1, tween='accelerate')
    
def fly_down(player, on_land):
    x, y = player.pos
    new_y = y + 50
    if new_y < 290:
        animate(player, pos=(x, new_y), duration=0.1, 
                tween='accelerate')
    else:
        animate(player, pos=(x, 304), duration=0.1, tween='accelerate')
        on_land()

def kick(player, on_land):
    player.kicking = True
    clock.schedule_unique(on_land, 0.6)
    
def land(player, on_land):
    x, y = player.pos
    animate(player, pos=(x, 304), duration=0.2, tween='accelerate')
    on_land()

def red_land():
    land(red, red_reset)

def red_reset():
    red.jumping = False
    red.flying = False
    red.kicking = False

def red_jump():
    jump(red, red_fall)

def red_fall():
    fall(red, red_reset)
    
def red_fly_up():
    fly_up(red)
    if not red.flying:
        red.flying = True
        clock.schedule_unique(red_land, FLIGHT_TIME)

def red_fly_down():
    fly_down(red, red_land)
    
def red_kick():
    kick(red, red_reset)

def blue_land():
    land(blue, blue_reset)
    
def blue_jump():
    jump(blue, blue_fall)

def blue_fall():
    fall(blue, blue_reset)
    
def blue_reset():
    blue.jumping = False
    blue.flying = False
    blue.kicking = False
    
def blue_fly_up():
    fly_up(blue)
    if not blue.flying:
        blue.flying = True
        clock.schedule_unique(blue_land, FLIGHT_TIME)

def blue_fly_down():
    fly_down(blue, blue_land)
    
def blue_kick():
    kick(blue, blue_reset)

def update():
    """
    Update game state in light of user input.
    """
    global active_objects
    # RED
    if keyboard[keys.RETURN] and not red.jumping:
        red_jump()
    if keyboard[keys.UP] and not red.jumping:
        red_fly_up()
    if keyboard[keys.DOWN]:
        red_fly_down()
    if (keyboard[keys.RIGHT] and not red.kicking and 
            not red.flying):
        red_kick()
    # Blue
    if keyboard[keys.SPACE] and not blue.jumping:
        blue_jump()
    if keyboard[keys.W] and not blue.jumping:
        blue_fly_up()
    if keyboard[keys.S]:
        blue_fly_down()
    if (keyboard[keys.D] and not blue.kicking and 
            not blue.flying):
        blue_kick()
    # Check for collisions between players and non-player objects.
    for obj in active_objects:
        # The object has scrolled past.
        if obj.right < 0:
            active_objects.remove(obj)
        # The object has been kicked forward.
        if obj.left > 1999:
            active_objects.remove(obj)
        # Red player collision
        if red.colliderect(obj) and not obj.red_hit:
            if red.kicking:
                x = random.randint(2000, 4000)
                y = random.randint(0, HEIGHT)
                animate(obj, pos=(x, y), duration=0.2, tween='accelerate')
            else:
                red.left -= FALL
                obj.red_hit = True
                if red.flying:
                    red_land()
        # Blue player collision.
        if blue.colliderect(obj) and not obj.blue_hit:
            if blue.kicking:
                x = random.randint(2000, 4000)
                y = random.randint(0, HEIGHT)
                animate(obj, pos=(x, y), duration=0.2, tween='accelerate')
            else:
                blue.left -= FALL
                obj.blue_hit = True
                if blue.flying:
                    blue_land()
    if random.randint(0, object_frequency) == 0:
        obj_collection = objects[random.choice(list(objects.keys()))]    
        low = obj_collection['pos'][0]
        high = obj_collection['pos'][1]
        new_object = Actor(random.choice(obj_collection['items']), 
                           pos=(1024, random.randint(low, high)))
        new_object.red_hit = False
        new_object.blue_hit = False
        active_objects.append(new_object)

def draw():
    """
    Draw things on the screen.
    """
    screen.blit('paper', (0, 0))
    red.draw()
    blue.draw()
    floor_a.draw()
    floor_b.draw()
    for obj in active_objects:
        obj.draw()

# Start the race.
clock.schedule_unique(animate_update, 0.08)