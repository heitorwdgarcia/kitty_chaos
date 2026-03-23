import pygame
import math
import random
from entities.pickup import Pickup
from core import game_state as gs
from settings import *

from systems.run_logger import (
    log_ammo,
    log_gem
)

from meta.rewards import reward_gems

# =========================================================
# REQUEST SYSTEM (CENTRALIZA SPAWN)
# =========================================================

def request_spawn_pickup(x, y, kind, priority=1, offset=0, force=False):

    # segurança (caso algo chame antes do world iniciar)
    if not hasattr(gs, "pending_pickups"):
        gs.pending_pickups = []

    gs.pending_pickups.append({
        "x": x,
        "y": y,
        "kind": kind,
        "priority": priority,
        "offset": offset,
        "force": force
    })

def update_pickups():

    player_rect = pygame.Rect(
        gs.player_x,
        gs.player_y,
        PLAYER_W,
        PLAYER_H
    )

    for p in gs.pickups[:]:
        # atualizar física do pickup
        p.update()
        # =================================================
        # MAGNET SYSTEM
        # =================================================

        if gs.pickup_magnet_radius > 0:

            dx = gs.player_x - p.x
            dy = gs.player_y - p.y

            dist = math.hypot(dx, dy)

            if dist < gs.pickup_magnet_radius and dist > 0:

                p.x += dx * 0.08
                p.y += dy * 0.08

        # -------------------------------------------------
        # UPDATE PICKUP PHYSICS
        # -------------------------------------------------

        size = int(20 * gs.pickup_size_mult)

        pickup_rect = pygame.Rect(
            p.x,
            p.y,
            size,
            size
        )

        # =================================================
        # PLAYER COLLECTS PICKUP
        # =================================================

        if pickup_rect.colliderect(player_rect):

            # ---------------- AMMO ----------------

            if p.kind == "ammo":

                ammo_gain = 5

                gs.ammo += ammo_gain
                gs.ammo = min(gs.ammo, gs.max_ammo)

                log_ammo(ammo_gain)

            # ---------------- GEM ----------------

            elif p.kind == "gem":

                amount = 1

                if gs.double_gems:
                    amount *= 2

                amount = int(amount * gs.gem_value_mult)

                reward_gems(amount)

                log_gem()

            # remove pickup
            gs.pickups.remove(p)
            continue

        # =================================================
        # REMOVE EXPIRED PICKUPS
        # =================================================

        if p.life <= 0:

            gs.pickups.remove(p)

# =========================================================
# CENTRAL SPAWN PROCESSOR (CÉREBRO)
# =========================================================

def process_pickup_spawns():

    if not hasattr(gs, "pending_pickups"):
        return

    if not gs.pending_pickups:
        return

    # =====================================================
    # 1. SEPARAR REQUESTS
    # =====================================================

    requests = gs.pending_pickups

    force_requests = [r for r in requests if r.get("force")]
    normal_requests = [r for r in requests if not r.get("force")]

    # =====================================================
    # 2. PROCESSAR FORCE (ANTI-SOFTLOCK)
    # =====================================================

    for r in force_requests:

        x = r["x"]
        y = r["y"]
        kind = r["kind"]
        offset = r.get("offset", 0)

        gs.pickups.append(Pickup(x + offset, y, kind))

    # =====================================================
    # 3. CALCULAR ESTADO (AMMO)
    # =====================================================

    ammo_on_ground = sum(
        1 for p in gs.pickups
        if getattr(p, "kind", None) == "ammo"
    )

    AMMO_VALUE = 5

    ammo_effective = gs.ammo + (ammo_on_ground * AMMO_VALUE)

    max_ammo = max(1, gs.max_ammo)
    missing_ammo = max_ammo - ammo_effective

    # =====================================================
    # 4. SE NÃO PRECISA, ENCERRA
    # =====================================================

    if missing_ammo <= 0:
        gs.pending_pickups.clear()
        return

    # =====================================================
    # 5. BUDGET
    # =====================================================

    spawn_budget = max(0, int(missing_ammo / AMMO_VALUE))

    if spawn_budget <= 0:
        gs.pending_pickups.clear()
        return

    # =====================================================
    # 6. PRIORIDADE
    # =====================================================

    requests = sorted(
        normal_requests,
        key=lambda r: r.get("priority", 1),
        reverse=True
    )

    # =====================================================
    # 7. CHANCE
    # =====================================================

    need_ratio = missing_ammo / max_ammo

    spawn_chance = 0.25 + (need_ratio * 0.6)
    spawn_chance = min(0.95, max(0.05, spawn_chance))

    # =====================================================
    # 8. PROCESSAR REQUESTS NORMAIS
    # =====================================================

    for r in requests:

        kind = r["kind"]

        # ---------------- AMMO ----------------

        if kind == "ammo":

            if spawn_budget > 0 and random.random() <= spawn_chance:

                x = r["x"]
                y = r["y"]
                offset = r.get("offset", 0)

                gs.pickups.append(Pickup(x + offset, y, "ammo"))

                spawn_budget -= 1

        # ---------------- OUTROS ----------------

        else:

            x = r["x"]
            y = r["y"]
            offset = r.get("offset", 0)

            gs.pickups.append(Pickup(x + offset, y, kind))

    # =====================================================
    # 9. LIMPAR FILA (FRAME-BASED)
    # =====================================================

    gs.pending_pickups.clear()
