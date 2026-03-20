from meta.save_data import load_save, save_game


# =========================================================
# SHOP ITEMS
# =========================================================

WEAPON_ITEMS = {

    "shotgun": 10,
    "smg": 20,
    "laser": 50
}


UPGRADE_ITEMS = {

    "rage_core": 15,
    "ghost_dash": 15,
    "pickup_magnet": 10,
    "combo_fire_rate": 20,
    "double_gems": 25
}


# =========================================================
# PLAYER DATA
# =========================================================

def get_player_gems():

    data = load_save()

    return data["gems"]


def get_unlocked_weapons():

    data = load_save()

    return data["weapons_unlocked"]


def get_unlocked_upgrades():

    data = load_save()

    return data["upgrades_unlocked"]


# =========================================================
# BUY WEAPON
# =========================================================

def buy_weapon(weapon):

    data = load_save()

    if weapon not in WEAPON_ITEMS:
        return False

    if weapon in data["weapons_unlocked"]:
        return False

    price = WEAPON_ITEMS[weapon]

    if data["gems"] < price:
        return False

    data["gems"] -= price

    data["weapons_unlocked"].append(weapon)

    save_game(data)

    return True


# =========================================================
# BUY UPGRADE
# =========================================================

def buy_upgrade(upgrade):

    data = load_save()

    if upgrade not in UPGRADE_ITEMS:
        return False

    if upgrade in data["upgrades_unlocked"]:
        return False

    price = UPGRADE_ITEMS[upgrade]

    if data["gems"] < price:
        return False

    data["gems"] -= price

    data["upgrades_unlocked"].append(upgrade)

    save_game(data)

    return True