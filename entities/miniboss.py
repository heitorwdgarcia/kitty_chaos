import math
from core import game_state as gs
from systems.boss_profiles import MINIBOSS_PROFILES


class MiniBoss:

    def __init__(self, x, y, profile="wander"):

        data = MINIBOSS_PROFILES.get(profile, MINIBOSS_PROFILES["wander"])

        hp = data["hp"]

        self.move_type = data["move"]
        self.speed = data["speed"]

        self.x = x
        self.y = y

        self.profile = profile

        self.max_hp = hp
        self.hp = hp

        # entity system
        self.is_hostile = True
        self.entity_type = "miniboss"

        self.timer = 0
        self.phase = 0

        self.width = 80
        self.height = 60

        # memória da luta
        self.start_kills = gs.kills
        self.start_timer = gs.run_timer

        self.near_miss = 0

        # telemetria
        self.shots_taken = 0
        self.shots_hit = 0


    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, base_speed=None):

        self.timer += 1

        # entrada na tela
        if self.y < 100:
            self.y += 2

        # -------------------------------------------------
        # MOVEMENT TYPES
        # -------------------------------------------------

        if self.move_type == "top":

            self.phase += 0.04
            self.x += math.sin(self.phase) * 3

        elif self.move_type == "wander":

            self.phase += 0.03
            self.x += math.sin(self.phase) * 4
            self.y += math.cos(self.phase) * 1.2

        elif self.move_type == "hunt":

            px = gs.player_x

            if px > self.x:
                self.x += self.speed * 2
            elif px < self.x:
                self.x -= self.speed * 2

        # -------------------------------------------------
        # LIMITES DA TELA
        # -------------------------------------------------

        if self.x < 0:
            self.x = 0

        if self.x > 600 - self.width:
            self.x = 600 - self.width


    # =====================================================
    # END FIGHT STATS
    # =====================================================

    def get_fight_stats(self):

        duration = (gs.run_timer - self.start_timer) / 60

        accuracy = 0.0

        if self.shots_taken > 0:
            accuracy = self.shots_hit / self.shots_taken

        stats = {

            "duration": duration,
            "near_miss": self.near_miss,
            "accuracy": accuracy

        }

        return stats