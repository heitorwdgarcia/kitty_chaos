import random

from core import game_state as gs
from settings import *

from entities.enemy import (
    NormalEnemy,
    TankEnemy,
    ZigZagEnemy
)


# =========================================================
# CENTRAL SPAWN AUTHORITY
# =========================================================

def spawn_enemy(enemy):
    gs.enemies.append(enemy)


# =========================================================
# SPAWN GROUP (CONTROLADO PELO DIRECTOR)
# =========================================================

def spawn_group(size, tier, intensity):

    for _ in range(size):

        x = spawn_position()

        enemy = choose_enemy(tier, x)

        apply_scaling(enemy, tier, intensity)

        spawn_enemy(enemy)


# =========================================================
# CHOOSE ENEMY TYPE
# =========================================================

def choose_enemy(tier, x):

    r = random.random()

    if tier == "early":

        if r < 0.15:
            return ZigZagEnemy(x, -40)

        return NormalEnemy(x, -40)

    elif tier == "mid":

        if r < 0.25:
            return TankEnemy(x, -40)

        elif r < 0.55:
            return ZigZagEnemy(x, -40)

        return NormalEnemy(x, -40)

    elif tier == "late":

        if r < 0.35:
            return TankEnemy(x, -40)

        elif r < 0.70:
            return ZigZagEnemy(x, -40)

        return NormalEnemy(x, -40)

    return NormalEnemy(x, -40)


# =========================================================
# SCALING SYSTEM (CORE DO BALANCE)
# =========================================================

def apply_scaling(enemy, tier, intensity):

    # ---------------- TIER BASE ----------------

    if tier == "early":
        tier_mult = 1.0
    elif tier == "mid":
        tier_mult = 1.6
    elif tier == "late":
        tier_mult = 2.4
    else:
        tier_mult = 1.0

    # ---------------- INTENSITY ----------------

    intensity_mult = 1 + (intensity * 1.8)

    # ---------------- BASE HP ----------------

    base_hp = getattr(enemy, "base_hp", 1)

    # ---------------- FINAL ----------------

    enemy.hp = int(base_hp * tier_mult * intensity_mult)
    enemy.hp = max(1, enemy.hp)


# =========================================================
# SPAWN POSITION
# =========================================================

def spawn_position():
    return random.randint(0, WIDTH - ENEMY_W)