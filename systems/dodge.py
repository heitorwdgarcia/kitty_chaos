from core import game_state as gs
from settings import *

from systems.rage_system import trigger_rage_explosion
from systems.run_logger import log_near_miss, log_world_damage
from systems.world_integrity import apply_world_damage
from systems.damage_system import request_damage

def update_dodge():

    for enemy in gs.enemies[:]:

        if enemy.y > gs.player_y + PLAYER_H:

            enemy_center = enemy.x + ENEMY_W / 2
            player_center = gs.player_x + PLAYER_W / 2

            distance = abs(enemy_center - player_center)

            if distance < gs.near_miss_radius:

                log_near_miss()

                if gs.miniboss:
                    gs.miniboss.near_miss += 1

                gs.chaos += 2

                if gs.near_miss_ammo:
                    gs.ammo = min(gs.ammo + 1, gs.max_ammo)

                gs.pending_feedback.append({
                    "type": "near_miss",
                    "x": enemy.x,
                    "y": enemy.y
                })

                if gs.rage_level > 0:

                    cx = enemy.x + ENEMY_W / 2
                    cy = enemy.y + ENEMY_H / 2

                    trigger_rage_explosion(cx, cy)

            elif distance > 140:

                damage = 2

                apply_world_damage(damage)
                log_world_damage(damage)

                gs.world_leak_counter += 1


            if getattr(enemy, "is_dead", False):
                continue
            
            request_damage(enemy, 999, source="event_dodge", damage_type="execution")