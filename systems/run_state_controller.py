from core import game_state as gs
import systems.run_director as run_director
from systems.collisions import player_enemy_collision


def update_run_state():

    # -------------------------------------------------
    # PLAYER MORREU
    # -------------------------------------------------

    player_enemy_collision()

    # -------------------------------------------------
    # WORLD MORREU
    # -------------------------------------------------

    if gs.world_integrity <= 0:
        run_director.request_end_run("world_destroyed")
        return True

    return False