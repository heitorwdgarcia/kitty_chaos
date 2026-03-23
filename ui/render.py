import pygame
import math
from core import game_state as gs
from settings import *
from entities.enemy import TankEnemy, ZigZagEnemy


def draw_entities(screen, offset_x=0, offset_y=0):

    # PLAYER

    pygame.draw.rect(
        screen,
        (80,160,255),
        (
            gs.player_x + offset_x,
            gs.player_y + offset_y,
            PLAYER_W,
            PLAYER_H
        )
    )

    # BULLETS

    for b in gs.bullets:

        pygame.draw.rect(
            screen,
            (255,230,50),
            (
                b.x + offset_x,
                b.y + offset_y,
                BULLET_W,
                BULLET_H
            )
        )

    # ENEMIES

    for e in gs.enemies:

        color = (220,60,60)

        if isinstance(e, TankEnemy):
            color = (60,160,60)

        elif isinstance(e, ZigZagEnemy):
            color = (200,60,255)

        w = ENEMY_W
        h = ENEMY_H

        if getattr(e, "is_golden", False):

            # -------------------------------------------------
            # PULSE EFFECT (FIXED)
            # -------------------------------------------------

            phase = getattr(e, "golden_phase", 0)

            # 🔥 FIX DO CRASH
            if not isinstance(phase, (int, float)):
                phase = 0.0

            pulse = math.sin(phase) * 0.05

            scale = getattr(e, "golden_scale", 1.2) + pulse

            w = int(ENEMY_W * scale)
            h = int(ENEMY_H * scale)

            # -------------------------------------------------
            # FLASH IF INVULNERABLE
            # -------------------------------------------------

            if getattr(e, "invulnerable", False):

                if int(phase * 6) % 2 == 0:
                    color = (255,255,200)
                else:
                    color = (255,210,80)

            else:
                color = (255,210,80)

        pygame.draw.rect(
            screen,
            color,
            (
                e.x + offset_x - (w - ENEMY_W)//2,
                e.y + offset_y - (h - ENEMY_H)//2,
                w,
                h
            )
        )

        # -------------------------------------------------
        # GOLDEN OUTLINE
        # -------------------------------------------------

        if getattr(e, "is_golden", False):

            pygame.draw.rect(
                screen,
                (255,255,200),
                (
                    e.x + offset_x - (w - ENEMY_W)//2 - 2,
                    e.y + offset_y - (h - ENEMY_H)//2 - 2,
                    w + 4,
                    h + 4
                ),
                2
            )

    # MINIBOSS

    if gs.miniboss:

        pygame.draw.rect(
            screen,
            (255,140,60),
            (
                gs.miniboss.x + offset_x,
                gs.miniboss.y + offset_y,
                gs.miniboss.width,
                gs.miniboss.height
            )
        )

    # BOSS

    if gs.boss:

        pygame.draw.rect(
            screen,
            (255,80,120),
            (
                gs.boss.x + offset_x,
                gs.boss.y + offset_y,
                80,
                60
            )
        )

    # LASER CHARGE

    if gs.laser_charging:

        px = gs.player_x + PLAYER_W // 2 + offset_x
        py = gs.player_y + offset_y

        pygame.draw.circle(screen, (80,200,255), (px,py), 6)
        pygame.draw.circle(screen, (150,255,255), (px,py), 10, 2)

    # LASER

    if gs.laser_active:

        lx = gs.laser_x + offset_x
        top = gs.player_y - gs.laser_length + offset_y

        pygame.draw.line(
            screen,
            (100,255,255),
            (lx, gs.player_y + offset_y),
            (lx, top),
            5
        )

    # PICKUPS

    for p in gs.pickups:

        x = p.x + offset_x
        y = p.y + offset_y

        if p.kind == "ammo":

            pygame.draw.rect(
                screen,
                (80,180,255),
                (x, y, 16, 16)
            )

        elif p.kind == "gem":

            pygame.draw.circle(
                screen,
                (220,40,40),
                (int(x + 5), int(y + 5)),
                5
            )

        else:

            pygame.draw.rect(
                screen,
                (80,255,120),
                (x, y, 14, 14)
            )

    # PARTICLES

    for p in gs.particles:

        pygame.draw.circle(
            screen,
            (255,200,50),
            (
                int(p.x + offset_x),
                int(p.y + offset_y)
            ),
            2
        )