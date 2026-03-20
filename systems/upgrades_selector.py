import random

from systems.upgrades_data import UPGRADES
from meta.shop import get_unlocked_upgrades

# ---------------------------------------------------------
# FILTROS BÁSICOS
# ---------------------------------------------------------

def is_upgrade_valid(upgrade_id, player_upgrades, current_weapon):

    u = UPGRADES[upgrade_id]

    unlocked = get_unlocked_upgrades()

    # -------------------------------------------------
    # SHOP LOCK
    # -------------------------------------------------

    if u["group"] == "shop" and upgrade_id not in unlocked:
        return False

    # -------------------------------------------------
    # WEAPON FILTER
    # -------------------------------------------------

    if u["weapon"] and u["weapon"] != current_weapon:
        return False

    # -------------------------------------------------
    # DEPENDENCY
    # -------------------------------------------------

    if u["requires"] and u["requires"] not in player_upgrades:
        return False

    # -------------------------------------------------
    # DUPLICATE PREVENTION
    # -------------------------------------------------

    if upgrade_id in player_upgrades:
        return False

    return True


# ---------------------------------------------------------
# PESO BASE + ADAPTATIVO
# ---------------------------------------------------------

def calculate_weight(upgrade, gs):

    weight = upgrade["base_weight"]

    # -------------------------------------
    # AMMO LOW
    # -------------------------------------

    if gs.ammo < gs.max_ammo * 0.3:
        if "ammo" in upgrade["tags"]:
            weight += 2

    # -------------------------------------
    # HP LOW
    # -------------------------------------

    if gs.player_hp < gs.player_max_hp * 0.4:
        if upgrade["category"] == "defense":
            weight += 2

    # -------------------------------------
    # BUILD DETECTION
    # -------------------------------------

    player_tags = gs.build_tags

    for tag in upgrade["tags"]:
        if tag in player_tags:
            weight += 1

    return max(weight, 0.1)


# ---------------------------------------------------------
# WEIGHTED RANDOM
# ---------------------------------------------------------

def weighted_choice(candidates):

    total = sum(w for _, w in candidates)

    r = random.uniform(0, total)

    upto = 0

    for upgrade_id, weight in candidates:

        if upto + weight >= r:
            return upgrade_id

        upto += weight

    return candidates[-1][0]


# ---------------------------------------------------------
# GERAR LISTA DE CANDIDATOS
# ---------------------------------------------------------

def get_valid_upgrades(gs):

    valid = []

    for upgrade_id in UPGRADES:

        if is_upgrade_valid(
            upgrade_id,
            gs.player_upgrades,
            gs.weapon
        ):
            valid.append(upgrade_id)

    return valid


# ---------------------------------------------------------
# SEPARAR WEAPON E GLOBAL
# ---------------------------------------------------------

def split_weapon_and_global(valid):

    weapon = []
    global_u = []

    for u in valid:

        if UPGRADES[u]["group"] == "weapon":
            weapon.append(u)
        else:
            global_u.append(u)

    return weapon, global_u


# ---------------------------------------------------------
# GERAR CHOICES
# ---------------------------------------------------------

def generate_upgrade_choices(gs):

    valid = get_valid_upgrades(gs)

    weapon_upgrades, global_upgrades = split_weapon_and_global(valid)

    choices = []

    # -----------------------------------------------------
    # TENTAR GERAR 1 WEAPON UPGRADE
    # -----------------------------------------------------

    if weapon_upgrades:

        weighted = []

        for u in weapon_upgrades:

            weight = calculate_weight(UPGRADES[u], gs)

            weighted.append((u, weight))

        selected = weighted_choice(weighted)

        choices.append(selected)

        weapon_upgrades.remove(selected)

    # -----------------------------------------------------
    # GERAR GLOBAL UPGRADES
    # -----------------------------------------------------

    remaining_slots = 3 - len(choices)

    pool = global_upgrades

    for _ in range(remaining_slots):

        if not pool:
            break

        weighted = []

        for u in pool:

            weight = calculate_weight(UPGRADES[u], gs)

            weighted.append((u, weight))

        selected = weighted_choice(weighted)

        choices.append(selected)

        pool.remove(selected)

    return choices