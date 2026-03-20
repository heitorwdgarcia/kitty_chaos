import pygame
import math

from core import game_state as gs
from settings import *

from systems.run_logger import (
    log_ammo,
    log_gem
)

from meta.rewards import reward_gems


def update_pickups():

    player_rect = pygame.Rect(
        gs.player_x,
        gs.player_y,
        PLAYER_W,
        PLAYER_H
    )

    for p in gs.pickups[:]:
        # atualizar física do pickup
        p.update()
        # =================================================
        # MAGNET SYSTEM
        # =================================================

        if gs.pickup_magnet_radius > 0:

            dx = gs.player_x - p.x
            dy = gs.player_y - p.y

            dist = math.hypot(dx, dy)

            if dist < gs.pickup_magnet_radius and dist > 0:

                p.x += dx * 0.08
                p.y += dy * 0.08

        # -------------------------------------------------
        # UPDATE PICKUP PHYSICS
        # -------------------------------------------------

        size = int(20 * gs.pickup_size_mult)

        pickup_rect = pygame.Rect(
            p.x,
            p.y,
            size,
            size
        )

        # =================================================
        # PLAYER COLLECTS PICKUP
        # =================================================

        if pickup_rect.colliderect(player_rect):

            # ---------------- AMMO ----------------

            if p.kind == "ammo":

                ammo_gain = 5

                gs.ammo += ammo_gain
                gs.ammo = min(gs.ammo, gs.max_ammo)

                log_ammo(ammo_gain)

            # ---------------- GEM ----------------

            elif p.kind == "gem":

                amount = 1

                if gs.double_gems:
                    amount *= 2

                amount = int(amount * gs.gem_value_mult)

                reward_gems(amount)

                log_gem()

            # remove pickup
            gs.pickups.remove(p)
            continue

        # =================================================
        # REMOVE EXPIRED PICKUPS
        # =================================================

        if p.life <= 0:

            gs.pickups.remove(p)