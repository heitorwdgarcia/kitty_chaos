import random

from entities.pickup import Pickup
from core import game_state as gs


# =========================================================
# ENEMY DROP SYSTEM
# =========================================================

def enemy_drop(enemy):

    x = enemy.x
    y = enemy.y

    ammo_chance = 0.18 + gs.ammo_drop_bonus
    gem_chance = 0.08

    # -------------------------------------------------
    # DURANTE BOSS FIGHT → mais ammo
    # -------------------------------------------------

    if gs.boss:
        ammo_chance = 0.30

    # -------------------------------------------------
    # MINIBOSS DROP (sempre dropa)
    # -------------------------------------------------

    if getattr(enemy, "is_miniboss", False):

        # gem garantida
        gs.pickups.append(Pickup(x, y, "gem"))

        # ammo garantida
        gs.pickups.append(Pickup(x + 12, y, "ammo"))

        # double pickups upgrade
        if gs.double_pickups:

            gs.pickups.append(Pickup(x + 6, y, "gem"))
            gs.pickups.append(Pickup(x + 18, y, "ammo"))

        return

    # -------------------------------------------------
    # NORMAL ENEMY DROPS
    # -------------------------------------------------

    if random.random() < ammo_chance:

        gs.pickups.append(Pickup(x, y, "ammo"))

        if gs.double_pickups:
            gs.pickups.append(Pickup(x + 6, y, "ammo"))

    if random.random() < gem_chance:

        gs.pickups.append(Pickup(x + 8, y, "gem"))

        if gs.double_pickups:
            gs.pickups.append(Pickup(x + 14, y, "gem"))