from core import game_state as gs
from settings import *


# =========================================================
# MOVE ENEMIES
# =========================================================

def move_enemies():

    enemy_speed = BASE_ENEMY_SPEED

    if DEBUG_MODE:
        enemy_speed *= DEBUG_ENEMY_SPEED

    for e in gs.enemies:
        e.update(enemy_speed)