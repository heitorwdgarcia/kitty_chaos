from core import game_state as gs
from settings import *


def update_laser():

    # =========================
    # CHARGING
    # =========================

    if gs.laser_charging:

        gs.laser_charge_timer -= 1

        if gs.laser_charge_timer <= 0:

            gs.laser_charging = False
            gs.laser_active = True

            gs.laser_timer = 18
            gs.laser_length = 0
            gs.laser_x = gs.player_x + PLAYER_W // 2

        return


    # =========================
    # ACTIVE
    # =========================

    if gs.laser_active:

        gs.laser_timer -= 1

        gs.laser_length += 40

        if gs.laser_length > HEIGHT:
            gs.laser_length = HEIGHT

        # laser follow upgrade
        if gs.laser_follow:
            gs.laser_x = gs.player_x + PLAYER_W // 2

        if gs.laser_timer <= 0:

            gs.laser_active = False