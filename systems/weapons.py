from core import game_state as gs
from entities.bullet import Bullet


# =========================================================
# PISTOL
# =========================================================

def fire_pistol(bx, by, hits, damage):

    gs.bullets.append(
        Bullet(bx, by, damage=damage, pierce=hits)
    )


# =========================================================
# SHOTGUN
# =========================================================

def fire_shotgun(bx, by, hits, damage):

    spread = 12 + gs.shotgun_spread

    bullets = [
        Bullet(bx - spread, by, damage=damage, pierce=hits),
        Bullet(bx, by, damage=damage, pierce=hits),
        Bullet(bx + spread, by, damage=damage, pierce=hits),
    ]

    for b in bullets:
        gs.bullets.append(b)

    # DOUBLE BLAST

    if gs.shotgun_double:

        extra = [
            Bullet(bx - spread * 1.5, by, damage=damage, pierce=hits),
            Bullet(bx + spread * 1.5, by, damage=damage, pierce=hits),
        ]

        for b in extra:
            gs.bullets.append(b)


# =========================================================
# SMG
# =========================================================

def fire_smg(bx, by, hits, damage):

    bullets = 1 + gs.smg_extra_bullets

    if gs.combo_boost and gs.combo >= 2:
        bullets += 1

    for i in range(bullets):

        offset = (i - bullets / 2) * 4

        gs.bullets.append(
            Bullet(
                bx + offset,
                by,
                damage=damage,
                pierce=hits
            )
        )


# =========================================================
# LASER
# =========================================================

def fire_laser(bx, by, hits, damage):

    # não pode disparar se já estiver carregando ou ativo
    if gs.laser_active or gs.laser_charging:
        return

    # aplica upgrade de cooldown
    charge_time = int(15 * gs.laser_cooldown_mult)

    gs.laser_charging = True
    gs.laser_charge_timer = charge_time


# =========================================================
# WEAPON REGISTRY
# =========================================================

WEAPON_FIRE = {

    "pistol": fire_pistol,
    "shotgun": fire_shotgun,
    "smg": fire_smg,
    "laser": fire_laser

}


# =========================================================
# SHOOT WEAPON
# =========================================================

def shoot_weapon(bx, by, weapon, hits, damage):

    fire = WEAPON_FIRE.get(weapon)

    if fire:
        fire(bx, by, hits, damage)