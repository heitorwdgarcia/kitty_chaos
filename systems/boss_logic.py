from core import game_state as gs
import random

from entities.enemy import NormalEnemy, ZigZagEnemy
import systems.run_director as run_director


def update_boss():

    boss = gs.boss

    if not boss:
        return

    boss.update()

    # ---------------------------------
    # SPAWN MINIONS
    # ---------------------------------

    if boss.timer % 150 == 0:

        spawn_minions(boss)


def spawn_minions(boss):

    if len(gs.enemies) > 10:
        return

    for _ in range(2):

        offset = random.randint(-120, 120)

        x = boss.x + offset

        r = random.random()

        if r < 0.4:
            enemy = ZigZagEnemy(x, boss.y + 60)
        else:
            enemy = NormalEnemy(x, boss.y + 60)

        gs.enemies.append(enemy)