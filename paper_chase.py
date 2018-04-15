"""
Paper Chase.
"""
score = 0
frame = 1
WIDTH = 1025
HEIGHT = 768
UPDATE = 0.08
SPEED = 10

stickperson = Actor('still')
stickperson.pos = 0, 96

def update_stick():
    global frame
    global score
    score += 1
    stickperson.image = "run{}".format(frame)
    frame += 1
    if frame > 4:
        frame = 1
    stickperson.left += SPEED
    if stickperson.left > WIDTH:
        stickperson.left = 0

clock.schedule_interval(update_stick, UPDATE)

def draw():
    screen.blit('paper', (0, 0))
    stickperson.draw()