"""
Paper Chase.
"""
WIDTH = 1024
HEIGHT = 384
SPEED = 20

stickperson = Actor('run1')
stickperson.pos = 512, 304
stickperson.score = 0
stickperson.frame = 1
stickperson.jumping = False
stickperson.flying = False
stickperson.kicking = False
floor_a = Actor('floor')
floor_a.pos = 0, 288
floor_b = Actor('floor')
floor_b.pos = 1024, 288

def animate_update():
    stickperson.score += 1
    if stickperson.jumping:
        stickperson.image = "run3"
    elif stickperson.kicking:
        stickperson.image = "kick"
    else:
        if stickperson.flying:
            stickperson.image = "fly{}".format(stickperson.frame)
        else:
            stickperson.image = "run{}".format(stickperson.frame)
        stickperson.frame += 1
        if stickperson.frame > 5:
            stickperson.frame = 1
    floor_a.left -= SPEED
    floor_b.left -= SPEED
    if int(floor_a.right) < 0:
        floor_a.left = floor_b.right
    if int(floor_b.right) < 0:
        floor_b.left = floor_a.right
    clock.schedule_unique(animate_update, 0.08)

clock.schedule_unique(animate_update, 0.08)

def jump():
    if not stickperson.flying:
        stickperson.jumping = True
        animate(stickperson, pos=(512, 204), duration=0.5, on_finished=fall, tween='decelerate')

def fall():
    animate(stickperson, pos=(512, 304), duration=0.3, on_finished=land, tween='accelerate')
    
def land():
    stickperson.jumping = False
    stickperson.flying = False
    stickperson.kicking = False

def fly_up():
    _, height = stickperson.pos
    animate(stickperson, pos=(512, max(20, height - 50)), duration=0.1, tween='accelerate')
    
def fly_down():
    _, height = stickperson.pos
    new_height = height + 50
    if new_height < 290:
        animate(stickperson, pos=(512, new_height), duration=0.1, tween='accelerate')
    else:
        animate(stickperson, pos=(512, 304), duration=0.1, tween='accelerate')
        land()
        
def kick():
    stickperson.kicking = True
    clock.schedule_unique(land, 0.6)

def update():
    if keyboard[keys.SPACE] and not stickperson.jumping:
        jump()
    if keyboard[keys.UP]:
        stickperson.flying = True
        fly_up()
    if keyboard[keys.DOWN]:
        fly_down()
    if keyboard[keys.RIGHT] and not stickperson.kicking and not stickperson.flying:
        kick()

def draw():
    screen.blit('paper', (0, 0))
    stickperson.draw()
    floor_a.draw()
    floor_b.draw()