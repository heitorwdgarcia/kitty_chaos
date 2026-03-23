from core import game_state as gs
from systems.pickups import request_spawn_pickup


def update_combo():

    if gs.combo_timer > 0:
        gs.combo_timer -= 1
    else:
        gs.combo = 0
        gs._last_combo_shown = 0

def combo_reward():

    reward = 0

    if gs.combo == 2:
        reward = 1

    elif gs.combo == 4:
        reward = 2

    elif gs.combo == 6:
        reward = 3

    elif gs.combo == 10:
        reward = 5

    if gs.combo_ammo and gs.combo >= 4:
        reward += 2 + gs.combo // 5

    if reward > 0:

        # 🔥 HARD CAP (evita flood de request)
        reward = min(reward, 1)

        for i in range(reward):

            request_spawn_pickup(
                gs.player_x,
                gs.player_y - 40,
                "ammo",
                priority=3,
                offset=i * 10
            )