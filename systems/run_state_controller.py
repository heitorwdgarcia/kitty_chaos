from core import game_state as gs

from systems.collisions import player_enemy_collision
from systems.run_ender import end_current_run


def update_run_state():

    # -------------------------------------------------
    # PLAYER MORREU
    # -------------------------------------------------

    if player_enemy_collision():
        end_current_run("enemy_collision")
        return True

    # -------------------------------------------------
    # WORLD MORREU
    # -------------------------------------------------

    if gs.world_integrity <= 0:
        end_current_run("world_destroyed")
        return True

    return False