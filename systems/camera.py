import random
from core import game_state as gs


def update_camera():

    if gs.screen_shake > 0:

        gs.screen_shake -= 1

        target_x = random.uniform(-gs.screen_shake_power, gs.screen_shake_power)
        target_y = random.uniform(-gs.screen_shake_power, gs.screen_shake_power)

        gs.camera_x += (target_x - gs.camera_x) * 0.4
        gs.camera_y += (target_y - gs.camera_y) * 0.4

    else:

        gs.camera_x *= 0.85
        gs.camera_y *= 0.85


def get_camera_offset():

    return int(gs.camera_x), int(gs.camera_y)