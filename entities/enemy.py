import math
import random

from core import game_state as gs


# =========================================================
# BASE ENEMY
# =========================================================

class NormalEnemy:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.width = 40
        self.height = 40

        self.hp = 1
        self.base_hp = 1

        self.speed = 2

        self.is_hostile = True
        self.entity_type = "enemy"

        self.hit_timer = 0

        # ---------------- GOLDEN ----------------
        self.is_golden = False
        self.golden_active = False
        self.invulnerable = False
        self.golden_phase = None  # "rising" | "falling"


    # =========================================================
    # GOLDEN
    # =========================================================

    def make_golden(self):

        self.is_golden = True
        self.golden_active = True
        self.golden_phase = "rising"
        self.invulnerable = True

        # IMPACTO VISUAL
        gs.hit_stop = 10
        gs.screen_shake = 20
        gs.screen_shake_power = 6


    # =========================================================
    # UPDATE
    # =========================================================

    def update(self, base_speed):

        # =========================
        # GOLDEN BEHAVIOR
        # =========================

        if self.golden_active:

            # ---------------- RISING ----------------
            if self.golden_phase == "rising":

                self.y -= 2  # subida lenta

                # chegou topo
                if self.y <= 40:
                    self.golden_phase = "falling"
                    self.invulnerable = False

            # ---------------- FALLING ----------------
            elif self.golden_phase == "falling":

                self.y += base_speed * 0.6  # descida lenta

                # colisão com outros inimigos
                for e in gs.enemies:

                    if e is self:
                        continue

                    if abs(e.x - self.x) < 30 and abs(e.y - self.y) < 30:
                        e.hp = 0  # explode


        else:
            # comportamento normal
            self.y += base_speed

        # =========================
        # HIT TIMER
        # =========================

        if self.hit_timer > 0:
            self.hit_timer -= 1


# =========================================================
# TANK ENEMY
# =========================================================

class TankEnemy(NormalEnemy):

    def __init__(self, x, y):
        super().__init__(x, y)

        self.base_hp = 2
        self.hp = 2


# =========================================================
# ZIG ZAG ENEMY
# =========================================================

class ZigZagEnemy(NormalEnemy):

    def __init__(self, x, y):
        super().__init__(x, y)

        self.base_x = x
        self.phase = random.random() * 10

        self.base_hp = 1.5
        self.hp = 1


    def update(self, base_speed):

        if self.golden_active:
            super().update(base_speed)
            return

        self.y += base_speed

        self.phase += 0.1
        self.x = self.base_x + math.sin(self.phase) * 40

        if self.hit_timer > 0:
            self.hit_timer -= 1