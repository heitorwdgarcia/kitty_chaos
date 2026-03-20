import random
from core import game_state as gs
from settings import WIDTH, PLAYER_W


def get_closest_enemy():

    closest = None
    dist = float("inf")

    targets = []

    # inimigos normais
    targets.extend(gs.enemies)

    # miniboss
    if gs.miniboss:
        targets.append(gs.miniboss)

    # boss
    if gs.boss:
        targets.append(gs.boss)

    # centro do player
    px = gs.player_x + PLAYER_W * 0.5
    py = gs.player_y + 20

    for e in targets:

        # centro aproximado do inimigo
        ex = e.x + getattr(e, "width", 40) * 0.5
        ey = e.y + getattr(e, "height", 40) * 0.5

        dx = ex - px
        dy = ey - py

        d = (dx * dx + dy * dy) ** 0.5

        if d < dist:
            dist = d
            closest = e

    return closest, dist


def move_left(speed=3):
    gs.player_x -= speed


def move_right(speed=3):
    gs.player_x += speed


def clamp_position():

    if gs.player_x < 0:
        gs.player_x = 0

    if gs.player_x > WIDTH - PLAYER_W:
        gs.player_x = WIDTH - PLAYER_W


def jitter(prob=0.02):

    if random.random() < prob:

        if random.random() < 0.5:
            move_left()
        else:
            move_right()