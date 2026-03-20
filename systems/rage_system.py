import math
import random

from core import game_state as gs

from systems.particles import spawn_hit_particles
from entities.pickup import Pickup

from systems.collisions import kill_enemy

from systems.run_logger import (
    log_rage_trigger,
    log_rage_kill
)


def trigger_rage_explosion(x, y):

    if gs.rage_level == 0:
        return

    radius = max(gs.rage_radius, 40)
    damage = gs.rage_damage

    # -------------------------------------------------
    # TELEMETRY
    # -------------------------------------------------

    log_rage_trigger()

    # -------------------------------------------------
    # VISUAL FX
    # -------------------------------------------------

    spawn_hit_particles(x, y)

    for enemy in gs.enemies[:]:

        dx = enemy.x - x
        dy = enemy.y - y

        dist = math.sqrt(dx*dx + dy*dy)

        if dist < radius:

            enemy.hp -= damage

            if enemy.hp <= 0:

                log_rage_kill()

                ex = enemy.x
                ey = enemy.y

                # usa sistema central de morte
                kill_enemy(enemy)

                # -------------------------------------------------
                # AMMO DROP
                # -------------------------------------------------

                if gs.rage_ammo:

                    if random.random() < 0.4:
                        gs.pickups.append(Pickup(ex, ey, "ammo"))

                # -------------------------------------------------
                # CHAIN EXPLOSION
                # -------------------------------------------------

                if gs.rage_chain:

                    if random.random() < 0.35:
                        trigger_rage_explosion(ex, ey)