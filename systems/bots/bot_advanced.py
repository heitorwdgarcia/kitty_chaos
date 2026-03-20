from core import game_state as gs
from systems.bots.bot_base import *

def update():

    gs.bot_shoot = False

    enemy, dist = get_closest_enemy()

    if not enemy:
        jitter(0.01)
        clamp_position()
        return

    # dodge cedo
    if dist < 200:

        if enemy.x < gs.player_x:
            move_right(5)
        else:
            move_left(5)

    # se inimigo estiver longe, alinhar com alvo
    else:

        if enemy.x < gs.player_x:
            move_left(4)
        else:
            move_right(4)


    # mira precisa
    if abs(enemy.x - gs.player_x) < 25:
        gs.bot_shoot = True

    clamp_position()