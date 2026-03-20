import pygame
import random

from core import game_state as gs
from settings import *

from systems.particles import spawn_hit_particles
from ui import spawn_message

from systems.run_logger import (
    log_kill,
    log_hit_enemy,
    log_player_hit,
    log_player_hp_loss
)

from systems.drop_system import enemy_drop


# =========================================================
# KILL ENEMY
# =========================================================

def kill_enemy(enemy):

    cx = enemy.x + ENEMY_W // 2
    cy = enemy.y + ENEMY_H // 2

    enemy_drop(enemy)

    if getattr(enemy, "is_golden", False):

        from systems.reward_system import spawn_chest
        spawn_chest()

    spawn_hit_particles(cx, cy)

    gs.kills += 1
    log_kill()

    gs.chaos += 0.3

    gs.combo += 1
    gs.combo_timer = int(60 * gs.combo_duration_mult)

    if gs.combo >= 2:
        spawn_message(
            f"COMBO x{gs.combo}",
            cx,
            cy - 20,
            (255, 220, 120)
        )

    from systems.combo import combo_reward
    combo_reward()

    if enemy in gs.enemies:
        gs.enemies.remove(enemy)


# =========================================================
# BULLET / LASER COLLISIONS
# =========================================================

def bullet_enemy_collision():

    # =========================================================
    # LASER COLLISION SYSTEM
    # =========================================================

    if gs.laser_active:

        pierce_left = 1 + gs.laser_pierce

        laser_rect = pygame.Rect(
            gs.laser_x - 3,
            gs.player_y - gs.laser_length,
            6,
            gs.laser_length
        )

        for enemy in gs.enemies[:]:

            enemy_rect = pygame.Rect(
                enemy.x,
                enemy.y,
                ENEMY_W,
                ENEMY_H
            )

            if laser_rect.colliderect(enemy_rect):

                if getattr(enemy, "golden_invulnerable", False):
                    continue

                enemy.hp -= gs.bullet_damage_mult
                enemy.hit_timer = 6

                log_hit_enemy()

                if enemy.hp <= 0:
                    kill_enemy(enemy)

                pierce_left -= 1

                if pierce_left <= 0:
                    gs.laser_active = False
                    break

        if gs.miniboss:

            miniboss_rect = pygame.Rect(
                gs.miniboss.x,
                gs.miniboss.y,
                gs.miniboss.width,
                gs.miniboss.height
            )

            if laser_rect.colliderect(miniboss_rect):

                gs.miniboss.hp -= gs.bullet_damage_mult
                log_hit_enemy()

                if gs.miniboss.hp <= 0:

                    from systems.nemesis_system import record_fight

                    stats = gs.miniboss.get_fight_stats()
                    record_fight(gs.miniboss.profile, stats)

                    gs.miniboss = None

        if gs.boss:

            boss_rect = pygame.Rect(
                gs.boss.x,
                gs.boss.y,
                gs.boss.width,
                gs.boss.height
            )

            if laser_rect.colliderect(boss_rect):

                gs.boss.hp -= gs.bullet_damage_mult
                gs.boss.hit_timer = 6

                log_hit_enemy()

                spawn_hit_particles(
                    gs.boss.x + random.randint(10, 70),
                    gs.boss.y + random.randint(10, 50)
                )


    # =========================================================
    # BULLET COLLISION SYSTEM
    # =========================================================

    for bullet in gs.bullets[:]:

        bullet_rect = pygame.Rect(
            bullet.x,
            bullet.y,
            BULLET_W,
            BULLET_H
        )

        for enemy in gs.enemies[:]:

            enemy_rect = pygame.Rect(
                enemy.x,
                enemy.y,
                ENEMY_W,
                ENEMY_H
            )

            if bullet_rect.colliderect(enemy_rect):

                if getattr(enemy, "golden_invulnerable", False):
                    continue

                enemy.hp -= bullet.damage
                enemy.hit_timer = 6

                if gs.weapon == "shotgun" and gs.shotgun_knockback > 0:
                    enemy.y += gs.shotgun_knockback

                log_hit_enemy()

                bullet.pierce -= 1

                if enemy.hp <= 0:
                    kill_enemy(enemy)

                if bullet.pierce <= 0:
                    if bullet in gs.bullets:
                        gs.bullets.remove(bullet)

                break

        if gs.boss:

            boss_rect = pygame.Rect(
                gs.boss.x,
                gs.boss.y,
                gs.boss.width,
                gs.boss.height
            )

            if bullet_rect.colliderect(boss_rect):

                gs.boss.hp -= bullet.damage
                gs.boss.hit_timer = 6

                log_hit_enemy()

                spawn_hit_particles(
                    gs.boss.x + random.randint(10, 70),
                    gs.boss.y + random.randint(10, 50)
                )

                if bullet in gs.bullets:
                    gs.bullets.remove(bullet)

        if gs.miniboss:

            miniboss_rect = pygame.Rect(
                gs.miniboss.x,
                gs.miniboss.y,
                gs.miniboss.width,
                gs.miniboss.height
            )

            if bullet_rect.colliderect(miniboss_rect):

                gs.miniboss.hp -= bullet.damage
                log_hit_enemy()

                if gs.miniboss.hp <= 0:

                    from systems.nemesis_system import record_fight

                    stats = gs.miniboss.get_fight_stats()
                    record_fight(gs.miniboss.profile, stats)

                    gs.miniboss = None

                if bullet in gs.bullets:
                    gs.bullets.remove(bullet)


# =========================================================
# PLAYER VS ENEMY
# =========================================================

def player_enemy_collision():

    if gs.player_iframes > 0:
        return False

    player_rect = pygame.Rect(
        gs.player_x,
        gs.player_y,
        PLAYER_W,
        PLAYER_H
    )

    for enemy in gs.enemies[:]:

        enemy_rect = pygame.Rect(
            enemy.x,
            enemy.y,
            ENEMY_W,
            ENEMY_H
        )

        if player_rect.colliderect(enemy_rect):

            if getattr(enemy, "is_golden", False):

                spawn_hit_particles(
                    enemy.x + ENEMY_W // 2,
                    enemy.y + ENEMY_H // 2
                )

                if enemy in gs.enemies:
                    gs.enemies.remove(enemy)

                return False

            log_player_hit()
            log_player_hp_loss(1)

            gs.player_hp -= 1

            if gs.ammo_on_damage:
                gs.ammo += 2
                gs.ammo = min(gs.ammo, gs.max_ammo)

            gs.player_iframes = gs.player_iframe_duration

            spawn_hit_particles(
                enemy.x + ENEMY_W // 2,
                enemy.y + ENEMY_H // 2
            )

            gs.screen_shake = 8
            gs.screen_shake_power = 6

            if enemy in gs.enemies:
                gs.enemies.remove(enemy)

            if gs.player_hp <= 0:
                return True

            return False

    return False