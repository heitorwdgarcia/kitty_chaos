from systems.upgrades_data import UPGRADES


def apply_upgrade(gs, upgrade_id):

    u = UPGRADES[upgrade_id]

    # registrar upgrade
    gs.player_upgrades.append(upgrade_id)

    # registrar tags da build
    for tag in u["tags"]:
        gs.build_tags.add(tag)

    # --------------------------------------------------
    # BASE UPGRADES
    # --------------------------------------------------

    if upgrade_id == "vitality":
        gs.player_max_hp += 1
        gs.player_hp += 1

    elif upgrade_id == "world_regen":
        gs.world_regen += 1

    elif upgrade_id == "ammo_pickup":
        gs.ammo_drop_bonus += 0.10

    elif upgrade_id == "near_miss_ammo":
        gs.near_miss_ammo = True

    elif upgrade_id == "near_miss_slow":
        gs.near_miss_slow = True

    elif upgrade_id == "gem_value":
        gs.gem_value_mult += 0.25

    elif upgrade_id == "ammo_capacity":
        gs.max_ammo += 3

    # --------------------------------------------------
    # SHOP UPGRADES
    # --------------------------------------------------

    elif upgrade_id == "rage_core":
        gs.rage_core = True

    elif upgrade_id == "rage_radius":
        gs.rage_radius += 20

    elif upgrade_id == "rage_chain":
        gs.rage_chain = True

    elif upgrade_id == "rage_ammo":
        gs.rage_ammo = True

    elif upgrade_id == "ghost_dash":
        gs.ghost_dash = True

    elif upgrade_id == "pickup_magnet":
        gs.pickup_magnet_radius += 60

    elif upgrade_id == "double_gems":
        gs.double_gems = True

    elif upgrade_id == "ammo_on_damage":
        gs.ammo_on_damage = True

    elif upgrade_id == "combo_fire_rate":
        gs.combo_fire_rate = True

    elif upgrade_id == "combo_ammo":
        gs.combo_ammo = True

    elif upgrade_id == "combo_damage":
        gs.combo_damage = True

    # --------------------------------------------------
    # PISTOL
    # --------------------------------------------------

    elif upgrade_id == "pistol_double":
        gs.double_shot = True

    elif upgrade_id == "pistol_pierce":
        gs.extra_pierce += 1

    elif upgrade_id == "pistol_rapid":
        gs.fire_rate_mult *= 0.8

    # --------------------------------------------------
    # SHOTGUN
    # --------------------------------------------------

    elif upgrade_id == "shotgun_spread":
        gs.shotgun_spread += 10

    elif upgrade_id == "shotgun_double":
        gs.shotgun_double = True

    elif upgrade_id == "shotgun_knockback":
        gs.shotgun_knockback += 5

    # --------------------------------------------------
    # SMG
    # --------------------------------------------------

    elif upgrade_id == "smg_overclock":
        gs.fire_rate_mult *= 0.75

    elif upgrade_id == "smg_stream":
        gs.smg_extra_bullets += 1

    elif upgrade_id == "smg_combo_boost":
        gs.combo_boost = True

    # --------------------------------------------------
    # LASER
    # --------------------------------------------------

    elif upgrade_id == "laser_cooldown":
        gs.laser_cooldown_mult *= 0.75

    elif upgrade_id == "laser_pierce":
        gs.laser_pierce += 1

    elif upgrade_id == "laser_follow":
        gs.laser_follow = True