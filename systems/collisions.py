import pygame
import random

from core import game_state as gs
from settings import *

from systems.particles import spawn_hit_particles


from systems.run_logger import (
    log_kill,
    log_hit_enemy,
    log_player_hit,
    log_player_hp_loss
)

from systems.damage_system import request_damage



# =========================================================
# BULLET / LASER COLLISIONS
# =========================================================

def bullet_enemy_collision():

    # =========================================================
    # LASER
    # =========================================================

    if gs.laser_active:

        pierce_left = 1 + gs.laser_pierce

        laser_rect = pygame.Rect(
            gs.laser_x - 3,
            gs.player_y - gs.laser_length,
            6,
            gs.laser_length
        )

        targets = []
        targets.extend(gs.enemies)

        if gs.miniboss:
            targets.append(gs.miniboss)

        if gs.boss:
            targets.append(gs.boss)

        for target in targets[:]:

            w = getattr(target, "width", ENEMY_W)
            h = getattr(target, "height", ENEMY_H)

            rect = pygame.Rect(target.x, target.y, w, h)

            if laser_rect.colliderect(rect):

                if getattr(target, "invulnerable", False):
                    continue

                request_damage(target, gs.bullet_damage_mult, source="laser")

                if hasattr(target, "hit_timer"):
                    target.hit_timer = 6

                pierce_left -= 1

                if pierce_left <= 0:
                    gs.laser_active = False
                    break

    # =========================================================
    # BULLET
    # =========================================================

    for bullet in gs.bullets[:]:

        bullet_rect = pygame.Rect(
            bullet.x,
            bullet.y,
            BULLET_W,
            BULLET_H
        )

        targets = []
        targets.extend(gs.enemies)

        if gs.miniboss:
            targets.append(gs.miniboss)

        if gs.boss:
            targets.append(gs.boss)

        for target in targets[:]:

            w = getattr(target, "width", ENEMY_W)
            h = getattr(target, "height", ENEMY_H)

            rect = pygame.Rect(target.x, target.y, w, h)

            if bullet_rect.colliderect(rect):

                if getattr(target, "invulnerable", False):
                    continue

                request_damage(target, bullet.damage, source="bullet")

                if hasattr(target, "hit_timer"):
                    target.hit_timer = 6

                bullet.pierce -= 1

                if bullet.pierce <= 0 and bullet in gs.bullets:
                    gs.bullets.remove(bullet)

                break


# =========================================================
# PLAYER VS ENEMY (AINDA VAI SER REFATORADO)
# =========================================================

def player_enemy_collision():

    # evita custo desnecessário
    if not gs.enemies:
        return

    player_rect = pygame.Rect(
        gs.player_x,
        gs.player_y,
        PLAYER_W,
        PLAYER_H
    )

    for enemy in gs.enemies[:]:

        # evita retrabalho
        if getattr(enemy, "is_dead", False):
            continue

        enemy_rect = pygame.Rect(
            enemy.x,
            enemy.y,
            ENEMY_W,
            ENEMY_H
        )

        if not player_rect.colliderect(enemy_rect):
            continue

        # -------------------------------------------------
        # GOLDEN (EVENT KILL)
        # -------------------------------------------------

        if getattr(enemy, "is_golden", False):

            spawn_hit_particles(
                enemy.x + ENEMY_W // 2,
                enemy.y + ENEMY_H // 2
            )

            request_damage(enemy, 999, source="event_golden", damage_type="execution")
            return  # uma colisão por frame já basta

        # -------------------------------------------------
        # PLAYER DAMAGE (PIPELINE)
        # -------------------------------------------------

        request_damage("player", 1, source="enemy_collision")

        # -------------------------------------------------
        # FEEDBACK VISUAL
        # -------------------------------------------------

        spawn_hit_particles(
            enemy.x + ENEMY_W // 2,
            enemy.y + ENEMY_H // 2
        )

        gs.pending_feedback.append({
            "type": "shake",
            "duration": 8,
            "power": 6
        })

        # -------------------------------------------------
        # EVENT KILL (DESIGN)
        # -------------------------------------------------

        request_damage(enemy, 999, source="event_collision", damage_type="execution")

        # uma colisão por frame evita spam
        return