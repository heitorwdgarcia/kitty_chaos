import random

from core import game_state as gs

from systems.particles import spawn_hit_particles
from entities.pickup import Pickup

from systems.run_logger import log_rage_trigger
from systems.damage_system import request_damage
from systems.pickups import request_spawn_pickup

def trigger_rage_explosion(x, y):

    if gs.rage_level == 0:
        return

    radius = max(gs.rage_radius, 40)
    radius_sq = radius * radius
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

        dist_sq = dx*dx + dy*dy

        if dist_sq < radius_sq:

            # =================================================
            # DAMAGE (PIPELINE CORRETO)
            # =================================================

            request_damage(enemy, damage, source="rage")

            ex = enemy.x
            ey = enemy.y

            # -------------------------------------------------
            # AMMO DROP
            # -------------------------------------------------

            if gs.rage_ammo:
                if random.random() < 0.4:
                    request_spawn_pickup(ex, ey, "ammo", priority=2)

            # -------------------------------------------------
            # CHAIN EXPLOSION
            # -------------------------------------------------

            if gs.rage_chain:
                if random.random() < 0.35:
                    trigger_rage_explosion(ex, ey)