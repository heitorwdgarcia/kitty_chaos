import random

from core import game_state as gs
from systems.spawn import spawn_group, spawn_enemy
from entities.enemy import TankEnemy
from entities.boss import Boss
from settings import WIDTH

import systems.run_director as run_director

from systems.run_logger import (
    log_miniboss,
    log_boss
)


# =========================================================
# COMBAT EVENT
# =========================================================

class CombatEvent:

    def __init__(self, duration):

        self.duration = duration
        self.timer = 0
        self.spawn_timer = 0

        self.golden_spawned = False


    def spawn_golden(self):

        candidates = [
            e for e in gs.enemies
            if not getattr(e, "is_golden", False)
        ]

        if candidates:
            enemy = random.choice(candidates)
        else:
            x = random.randint(40, WIDTH - 40)
            enemy = TankEnemy(x, -40)
            spawn_enemy(enemy)

        enemy.make_golden()

        self.golden_spawned = True


    def update(self):

        self.timer += 1
        self.spawn_timer += 1

        intensity = run_director.get_intensity()
        tier = run_director.get_tier()

        # ---------------- SPAWN RATE ----------------

        spawn_rate = int(90 - (50 * intensity))
        spawn_rate = max(18, spawn_rate)

        enemy_cap = int(5 + (8 * intensity))

        group_min = 1
        group_max = int(1 + (3 * intensity))

        # ---------------- SPAWN ----------------

        if self.spawn_timer >= spawn_rate:

            self.spawn_timer = 0

            if len(gs.enemies) < enemy_cap:

                group = random.randint(group_min, group_max)

                spawn_group(group, tier, intensity)

        # ---------------- GOLDEN ----------------

        if not self.golden_spawned and self.timer > self.duration * 30:
            self.spawn_golden()

        # ---------------- END ----------------

        if self.timer >= self.duration * 60:
            return True

        return False


# =========================================================
# ELITE EVENT
# =========================================================

class EliteEvent:

    def __init__(self):
        self.spawned = False

    def update(self):

        if not self.spawned:

            enemy = TankEnemy(WIDTH // 2, -40)
            enemy.make_golden()

            spawn_enemy(enemy)

            self.spawned = True

        if len(gs.enemies) == 0:
            return True

        return False


# =========================================================
# MINIBOSS EVENT
# =========================================================

class MinibossEvent:

    def __init__(self, profile=None):

        self.spawned = False
        self.profile = profile

    def update(self):

        if not self.spawned:

            from entities.miniboss import MiniBoss

            profile = self.profile or random.choice([
                "hunter",
                "wander",
                "top_guard"
            ])

            enemy = MiniBoss(WIDTH // 2, -80, profile)

            gs.miniboss = enemy

            log_miniboss()

            self.spawned = True

        if gs.miniboss is None:
            return True

        return False


# =========================================================
# BOSS EVENT
# =========================================================

class BossEvent:

    def __init__(self):
        self.spawned = False

    def update(self):

        if not self.spawned:

            # FIX correto: boss precisa de hp
            gs.boss = Boss(WIDTH // 2 - 40, -80, 40)

            log_boss()

            self.spawned = True

        if gs.boss is None:
            return True

        return False