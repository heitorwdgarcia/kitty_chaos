from core import game_state as gs
from systems.bots.bot_base import *

def update():

    gs.bot_shoot = False

    enemy, dist = get_closest_enemy()

    if not enemy:
        jitter(0.02)
        clamp_position()
        return

    # dodge melhor
    if dist < 140:

        if enemy.x < gs.player_x:
            move_right(4)
        else:
            move_left(4)

        # se inimigo estiver longe, alinhar com alvo
    else:

        if enemy.x < gs.player_x:
            move_left(3)
        else:
            move_right(3)

    # mira melhor
    if abs(enemy.x - gs.player_x) < 40:
        gs.bot_shoot = True

    clamp_position()