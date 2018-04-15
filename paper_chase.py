"""
Paper Chase.
"""
score = 0
frame = 1
WIDTH = 1025
HEIGHT = 384
UPDATE = 0.08
SPEED = 10

stickperson = Actor('still')
stickperson.pos = 512, 288
floor_a = Actor('floor')
floor_a.pos = 0, 288
floor_b = Actor('floor')
floor_b.pos = 2048, 288

def animate_update():
    global frame
    global score
    score += 1
    stickperson.image = "run{}".format(frame)
    frame += 1
    if frame > 4:
        frame = 1
    floor_a.left -= SPEED
    floor_b.left -= SPEED
    if int(floor_a.right) < 0:
        floor_a.left = floor_b.right
    if int(floor_b.right) < 0:
        floor_b.left = floor_a.right

clock.schedule_interval(animate_update, UPDATE)

def draw():
    screen.blit('paper', (0, 0))
    stickperson.draw()
    floor_a.draw()
    floor_b.draw()