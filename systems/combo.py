from core import game_state as gs


def update_combo():

    if gs.combo_timer > 0:

        gs.combo_timer -= 1

    else:

        gs.combo = 0


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
        
        reward = min(reward, 3)

        from entities.pickup import Pickup

        for i in range(reward):

            gs.pickups.append(
                Pickup(gs.player_x + i * 10, gs.player_y - 40, "ammo")
            )