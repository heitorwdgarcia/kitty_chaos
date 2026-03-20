import random
from core import game_state as gs
from systems.bots.bot_base import *

def update():

    gs.bot_shoot = False

    enemy, dist = get_closest_enemy()

    if not enemy:
        jitter(0.05)
        clamp_position()
        return

    # dodge tarde
    if dist < 80:

        if enemy.x < gs.player_x:
            move_right()
        else:
            move_left()

    # mira ruim
    if abs(enemy.x - gs.player_x) < 60:
        gs.bot_shoot = True

    jitter(0.05)

    clamp_position()