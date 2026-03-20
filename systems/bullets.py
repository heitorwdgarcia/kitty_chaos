from core import game_state as gs


def move_bullets():

    for b in gs.bullets:
        b.update()

    gs.bullets[:] = [b for b in gs.bullets if b.y > -20]