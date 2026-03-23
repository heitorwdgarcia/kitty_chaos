import random

from core import game_state as gs
from systems.pickups import request_spawn_pickup


# =========================================================
# ENEMY DROP SYSTEM (AGORA SÓ FAZ REQUEST)
# =========================================================

def enemy_drop(enemy):

    x = enemy.x
    y = enemy.y

    # -------------------------------------------------
    # CONFIG
    # -------------------------------------------------

    gem_chance = 0.08
    ammo_chance = 0.12  # 🔥 NOVO: estabilidade básica de ammo

    # -------------------------------------------------
    # MINIBOSS DROP (SEMPRE DROP)
    # -------------------------------------------------

    if getattr(enemy, "is_miniboss", False):

        request_spawn_pickup(x, y, "gem", priority=1)
        request_spawn_pickup(x + 12, y, "ammo", priority=4)

        if getattr(gs, "double_pickups", False):
            request_spawn_pickup(x + 6, y, "gem", priority=1)
            request_spawn_pickup(x + 18, y, "ammo", priority=4)

        return

    # -------------------------------------------------
    # GEM DROP (MANTÉM RNG SIMPLES)
    # -------------------------------------------------

    if random.random() < gem_chance:

        request_spawn_pickup(x + 8, y, "gem", priority=1)

        if getattr(gs, "double_pickups", False):
            request_spawn_pickup(x + 14, y, "gem", priority=1)

    # -------------------------------------------------
    # AMMO DROP (NOVO - LEVE)
    # -------------------------------------------------

    if random.random() < ammo_chance:

        request_spawn_pickup(x + 10, y, "ammo", priority=2)

        if getattr(gs, "double_pickups", False):
            request_spawn_pickup(x + 16, y, "ammo", priority=2)