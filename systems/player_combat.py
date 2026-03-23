import pygame

from core import game_state as gs
from settings import *

from systems.weapons import shoot_weapon
from systems.weapons_data import WEAPONS

from systems.run_logger import log_shot
from systems.pickups import request_spawn_pickup


# =========================================================
# HANDLE SHOOTING
# =========================================================

def handle_shooting(keys):

    weapon_data = WEAPONS[gs.weapon]

    # -------------------------------------------------
    # FIRE RATE MODIFIERS
    # -------------------------------------------------

    cooldown_mult = gs.fire_rate_mult

    if gs.combo_fire_rate and gs.combo >= 3:
        cooldown_mult *= 0.8

    shoot_cooldown = int(weapon_data["cooldown"] * cooldown_mult)

    hits = weapon_data["hits"] + gs.extra_pierce

    # -------------------------------------------------
    # INPUT (PLAYER OU BOT)
    # -------------------------------------------------

    shoot_pressed = keys[pygame.K_SPACE]

    if gs.bot_mode:
        shoot_pressed = gs.bot_shoot

    # -------------------------------------------------
    # DISPARO
    # -------------------------------------------------

    if shoot_pressed and (gs.ammo > 0 or DEBUG_MODE):

        if gs.shoot_timer <= 0:

            bx = gs.player_x + PLAYER_W // 2 - BULLET_W // 2
            by = gs.player_y

            # -------------------------------------------------
            # DAMAGE MODIFIERS
            # -------------------------------------------------

            damage = gs.bullet_damage_mult

            if gs.combo_damage and gs.combo >= 3:
                damage *= 1.5

            # -------------------------------------------------
            # FIRE WEAPON
            # -------------------------------------------------

            shoot_weapon(bx, by, gs.weapon, hits, damage)
            log_shot()

            # -------------------------------------------------
            # DOUBLE SHOT
            # -------------------------------------------------

            if gs.double_shot:

                shoot_weapon(bx - 10, by, gs.weapon, hits, damage)
                shoot_weapon(bx + 10, by, gs.weapon, hits, damage)

                log_shot()
                log_shot()

            # -------------------------------------------------
            # AMMO
            # -------------------------------------------------

            if not DEBUG_MODE:
                gs.ammo -= 1

            gs.shoot_timer = shoot_cooldown

    # -------------------------------------------------
    # COOLDOWN
    # -------------------------------------------------

    if gs.shoot_timer > 0:
        gs.shoot_timer -= 1

    # =========================================================
    # EMERGENCY AMMO REGEN (ANTI SOFTLOCK)
    # =========================================================

    # garante existência
    if not hasattr(gs, "ammo_starve_timer"):
        gs.ammo_starve_timer = 0

    if gs.ammo <= 0:

        gs.ammo_starve_timer += 1

        # 🔥 threshold dinâmico (entra antes se crítico)
        threshold = 120 if gs.ammo <= 2 else 180

        if gs.ammo_starve_timer > threshold:

            # verifica se já existe pickup de ammo na tela
            ammo_pickups = [
                p for p in gs.pickups
                if getattr(p, "kind", None) == "ammo"
            ]

            if len(ammo_pickups) == 0:

                request_spawn_pickup(
                    gs.player_x,
                    gs.player_y - 30,
                    "ammo",
                    priority=999,
                    force=True   # 🔥 ESSA É A CHAVE
                )

            # cooldown antes de poder spawnar outro
            gs.ammo_starve_timer = -60

    else:
        gs.ammo_starve_timer = 0