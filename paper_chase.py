"""
Paper Chase -- game logic.
"""
import random
from gamedata import *

music.play('running_music')  # So sorry... ;-)

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
    global power_up
    global END
    # Increase difficulty every LEVEL_UP steps.
    steps += 1
    if steps % LEVEL_UP == 0:
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
    # Move a power-up
    if power_up:
        power_up.left -= speed
        if power_up.right < 0:
            power_up = None
    # Check for winning condition
    distance_between_players = abs(red.left - blue.left)
    if (distance_between_players > DISTANCE or red.right < 0 or 
            blue.right < 0):
        END = True
    else:
        # Re-schedule a call to this function.
        clock.schedule_unique(animate_update, 0.08)

def toggle_warning():
    """
    Used to make the "Steps ahead" info flash.
    """
    global WARNING
    WARNING = not WARNING
    clock.schedule_unique(toggle_warning, 0.5)

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
    if not player.landing:
        x, y = player.pos
        animate(player, pos=(x, max(20, y - 50)), 
                duration=0.1, tween='accelerate')
    
def fly_down(player, on_land):
    if not player.landing:
        x, y = player.pos
        new_y = y + 50
        if new_y < 290:
            animate(player, pos=(x, new_y), duration=0.1, 
                    tween='accelerate')
        else:
            on_land()

def kick(player, on_land):
    player.kicking = True
    clock.schedule_unique(on_land, 0.6)
    
def land(player, on_land):
    player.landing = True
    x, y = player.pos
    animate(player, pos=(x, 304), duration=0.1, tween='accelerate',
            on_finished=on_land)

def red_land():
    land(red, red_reset)

def red_reset():
    red.jumping = False
    red.flying = False
    red.kicking = False
    red.landing = False

def red_jump():
    jump(red, red_fall)

def red_fall():
    fall(red, red_reset)
 
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
    blue.landing = False

def update():
    """
    Update game state in light of user input.
    """
    if END:  # The race has finished
        update_end()
    elif STARTED:  # The race has started
        update_race()
    else:  # Just display the intro screen
        update_intro()

def update_intro():
    """
    Wait for the space bar to be pressed and then start
    the race.
    """
    global STARTED
    if keyboard[keys.SPACE]:
        STARTED = True
        # Start the race.
        clock.schedule_unique(animate_update, 0.08)

def update_end():
    """
    Wait for the space bar to be pressed and then reset the
    game to the start state.
    """
    global STARTED
    global END
    global speed
    global object_frequency
    global steps
    global active_objects
    if keyboard[keys.SPACE]:
        STARTED = True
        END = False
        speed = 20  # How fast non-player objects move.
        object_frequency = 100  # Smaller = more frequent.
        steps = 0
        red.pos = (512, 304)
        blue.pos = (512, 304)
        red.flying = False
        blue.flying = False
        red.jumping = False
        blue.jumping = False
        red.antigravity = 0
        blue.antigravity = 0
        active_objects = []
        # Start the race.
        clock.schedule_unique(animate_update, 0.08)
    
def update_race():
    """
    Update game state when the players are racing.
    """
    global active_objects
    global power_up
    # RED
    if keyboard[keys.RETURN] and not red.jumping:
        red_jump()
    if keyboard[keys.UP] and not red.jumping:
        if red.antigravity > 0 and not red.flying:
            red.antigravity -= 1
            red.flying = True
            clock.schedule_unique(red_land, FLIGHT_TIME)
        if red.flying:
            fly_up(red)
    if keyboard[keys.DOWN]:
        fly_down(red, red_land)
    if (keyboard[keys.RIGHT] and not red.kicking and 
            not red.flying):
        kick(red, red_reset)
    # Blue
    if keyboard[keys.SPACE] and not blue.jumping:
        blue_jump()
    if keyboard[keys.W] and not blue.jumping:
        if blue.antigravity > 0 and not blue.flying:
            blue.antigravity -= 1
            blue.flying = True
            clock.schedule_unique(blue_land, FLIGHT_TIME)
        if blue.flying:
            fly_up(blue)
    if keyboard[keys.S]:
        fly_down(blue, blue_land)
    if (keyboard[keys.D] and not blue.kicking and 
            not blue.flying):
        kick(blue, blue_reset)
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
    # Check for collision with power-up.
    if power_up:
        # This may seem convoluted, but it ensures that if both players get to the
        # power-up at the same time the game is "fair" in balancing up the advantage.
        touching_red = (red.colliderect(power_up) and not (red.flying or red.kicking)
                        and red.antigravity < 3)
        touching_blue = (blue.colliderect(power_up) and not (blue.flying or blue.kicking)
                         and blue.antigravity < 3)
        if touching_blue and touching_red:
            if red.antigravity > blue.antigravity:
                blue.antigravity += 1
            elif red.antigravity < blue.antigravity:
                red.antigravity += 1
            else:
                if random.choice([True, False]):
                    red.antigravity += 1
                else:
                    blue.antigravity += 1
            power_up = None
        elif touching_red:
            red.antigravity += 1
            power_up = None
        elif touching_blue:
            blue.antigravity += 1
            power_up = None
    if random.randint(0, object_frequency) == 0 or not active_objects:
        make_obstacle(ground_objects)
    if random.randint(0, object_frequency) == 0 or not active_objects:
        make_obstacle(air_objects)
    if not power_up and random.randint(0, powerup_frequency) == 0:
        power_up = Actor('antigravity', pos=(1024, 320))

def make_obstacle(objects):
    global active_objects
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
    if END:  # The race has finished
        draw_end()
    elif STARTED:  # The race has started
        draw_race()
    else:  # Just display the intro screen
        draw_intro()

def draw_intro():
    """
    Draw the intro screen with the story, keys and instructions
    to press space to start the race.    
    """
    # Paper
    screen.draw.text('Paper', (260, 10),
                     fontname='funsized', fontsize=56,
                     color=(0, 0, 255), background='None')
    # Chase
    screen.draw.text('Chase', (500, 10),
                     fontname='funsized', fontsize=56,
                     color=(255, 0, 0), background='None')
    # Story
    story = ("The intergalactic war between the red and blue factions "
             "of the biro universe has reached its climax. Each world has "
             "sent a stick-figure champion to race in the \"Paper chase\" "
             "for ultimate victory and to decide which colour biro pen "
             "teachers should use when marking work. (Get {} steps ahead "
             "to win, collect up to 3 Python power-ups to import antigravity and "
             "avoid all other obstacles.)").format(DISTANCE)
    screen.draw.text(story, (50, 80), width=900,
                     fontname='rudiment', fontsize=30,
                     color=(0, 0, 0))
    screen.draw.text('W - fly up, S - fly down\nD - kick object, SPACE - jump.', (50, 240),
                     fontname='rudiment', fontsize=30,
                     color=(0, 0, 255))
    screen.draw.text('Up Arrow - fly up, Down Arrow - fly down\nRight Arrow - kick object, Enter - jump.', (500, 240),
                     fontname='rudiment', fontsize=30,
                     color=(255, 0, 0))                 
    screen.draw.text('Press SPACE to start the race.', (270, 320),
                     fontname='rudiment', fontsize=38,
                     color=(0, 0, 0), background='None')


def draw_end():
    """
    Draw the end state with the result and instructions to
    press space to start again.
    """
    winner = 'Red' if red.left > blue.left else 'Blue'
    color = (255, 0, 0) if red.left > blue.left else (0, 0, 255)
    screen.draw.text('{} won!'.format(winner), (360, 100),
                     fontname='funsized', fontsize=56,
                     color=color, background='None')
    screen.draw.text('Press SPACE to restart.', (360, 250),
                     fontname='rudiment', fontsize=38,
                     color=(0, 0, 0), background='None')
    
def draw_race():
    """
    Draw game state when players are racing.
    """
    red.draw()
    blue.draw()
    floor_a.draw()
    floor_b.draw()
    for obj in active_objects:
        obj.draw()
    if power_up:
        power_up.draw()
    screen.draw.text('Antigravity: {}'.format(red.antigravity),
                     (800, 340), fontname='rudiment', fontsize=38,
                     color=(255, 0, 0), background='None')
    screen.draw.text('Antigravity: {}'.format(blue.antigravity),
                     (580, 340), fontname='rudiment', fontsize=38,
                     color=(0, 0, 255), background='None')
    distance_between_players = int(abs(red.left - blue.left))
    distance_to_display = distance_between_players - (distance_between_players % 10)
    color = (255, 0, 0) if red.left > blue.left else (0, 0, 255)
    alert_margin = int((DISTANCE / 4) * 3)
    if distance_to_display < alert_margin:
        screen.draw.text('Steps ahead: {}'.format(distance_to_display),
                         (10, 340), fontname='rudiment', fontsize=38,
                         color=color, background='None')
    elif WARNING:
        screen.draw.text('Steps ahead: {}'.format(distance_to_display),
                         (10, 340), fontname='rudiment', fontsize=38,
                         color=color, background='None')

toggle_warning()