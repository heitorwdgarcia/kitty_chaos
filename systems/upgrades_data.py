UPGRADES = {

# -------------------------------------------------
# BASE UPGRADES (sempre disponíveis)
# -------------------------------------------------

"vitality": {
    "name": "Vitality",
    "group": "base",
    "category": "defense",
    "weapon": None,
    "tier": 1,
    "requires": None,
    "tags": ["hp", "defense"],
    "base_weight": 1.8
},

"world_regen": {
    "name": "World Regeneration",
    "group": "base",
    "category": "defense",
    "weapon": None,
    "tier": 1,
    "requires": None,
    "tags": ["world", "defense"],
    "base_weight": 1.8
},

"ammo_pickup": {
    "name": "Ammo Pickup+",
    "group": "base",
    "category": "ammo",
    "weapon": None,
    "tier": 1,
    "requires": None,
    "tags": ["ammo"],
    "base_weight": 2
},

"near_miss_ammo": {
    "name": "Near Miss Ammo",
    "group": "base",
    "category": "dodge",
    "weapon": None,
    "tier": 1,
    "requires": None,
    "tags": ["dodge", "ammo"],
    "base_weight": 1.6
},

"near_miss_slow": {
    "name": "Near Miss Slow",
    "group": "base",
    "category": "dodge",
    "weapon": None,
    "tier": 1,
    "requires": None,
    "tags": ["dodge", "control"],
    "base_weight": 1.6
},

"gem_value": {
    "name": "Gem Value+",
    "group": "base",
    "category": "economy",
    "weapon": None,
    "tier": 1,
    "requires": None,
    "tags": ["gem"],
    "base_weight": 1.2
},

"ammo_capacity": {
    "name": "Ammo Capacity",
    "group": "base",
    "category": "ammo",
    "weapon": None,
    "tier": 1,
    "requires": None,
    "tags": ["ammo"],
    "base_weight": 2
},

# -------------------------------------------------
# SHOP UPGRADES (comprados na loja)
# -------------------------------------------------

"rage_core": {
    "name": "Rage Core",
    "group": "shop",
    "category": "rage",
    "weapon": None,
    "tier": 1,
    "requires": None,
    "tags": ["rage"],
    "base_weight": 1
},

"rage_radius": {
    "name": "Rage Radius",
    "group": "shop",
    "category": "rage",
    "weapon": None,
    "tier": 2,
    "requires": "rage_core",
    "tags": ["rage", "damage"],
    "base_weight": 1
},

"rage_chain": {
    "name": "Rage Chain",
    "group": "shop",
    "category": "rage",
    "weapon": None,
    "tier": 2,
    "requires": "rage_core",
    "tags": ["rage"],
    "base_weight": 1
},

"rage_ammo": {
    "name": "Rage Ammo",
    "group": "shop",
    "category": "rage",
    "weapon": None,
    "tier": 2,
    "requires": "rage_core",
    "tags": ["rage", "ammo"],
    "base_weight": 1
},

"ghost_dash": {
    "name": "Ghost Dash",
    "group": "shop",
    "category": "dodge",
    "weapon": None,
    "tier": 1,
    "requires": None,
    "tags": ["dodge"],
    "base_weight": 1.6
},

"pickup_magnet": {
    "name": "Pickup Magnet",
    "group": "shop",
    "category": "economy",
    "weapon": None,
    "tier": 1,
    "requires": None,
    "tags": ["pickup"],
    "base_weight": 1.2
},

"double_gems": {
    "name": "Double Gems",
    "group": "shop",
    "category": "economy",
    "weapon": None,
    "tier": 1,
    "requires": None,
    "tags": ["gem"],
    "base_weight": 1.2
},

"ammo_on_damage": {
    "name": "Emergency Ammo",
    "group": "shop",
    "category": "ammo",
    "weapon": None,
    "tier": 1,
    "requires": None,
    "tags": ["ammo"],
    "base_weight": 2
},

"combo_fire_rate": {
    "name": "Combo Fire Rate",
    "group": "shop",
    "category": "damage",
    "weapon": None,
    "tier": 1,
    "requires": None,
    "tags": ["combo"],
    "base_weight": 2
},

"combo_ammo": {
    "name": "Combo Ammo",
    "group": "shop",
    "category": "ammo",
    "weapon": None,
    "tier": 2,
    "requires": "combo_fire_rate",
    "tags": ["combo", "ammo"],
    "base_weight": 2
},

"combo_damage": {
    "name": "Combo Damage",
    "group": "shop",
    "category": "damage",
    "weapon": None,
    "tier": 2,
    "requires": "combo_fire_rate",
    "tags": ["combo"],
    "base_weight": 2
},

# -------------------------------------------------
# WEAPON UPGRADES
# -------------------------------------------------

# PISTOL

"pistol_double": {
    "name": "Double Shot",
    "group": "weapon",
    "category": "damage",
    "weapon": "pistol",
    "tier": 1,
    "requires": None,
    "tags": ["damage"],
    "base_weight": 3
},

"pistol_pierce": {
    "name": "Piercing Shot",
    "group": "weapon",
    "category": "damage",
    "weapon": "pistol",
    "tier": 1,
    "requires": None,
    "tags": ["damage"],
    "base_weight": 3
},

"pistol_rapid": {
    "name": "Rapid Trigger",
    "group": "weapon",
    "category": "damage",
    "weapon": "pistol",
    "tier": 1,
    "requires": None,
    "tags": ["fire_rate"],
    "base_weight": 3
},

# SHOTGUN

"shotgun_spread": {
    "name": "Wide Spread",
    "group": "weapon",
    "category": "damage",
    "weapon": "shotgun",
    "tier": 1,
    "requires": None,
    "tags": ["spread"],
    "base_weight": 3
},

"shotgun_double": {
    "name": "Double Blast",
    "group": "weapon",
    "category": "damage",
    "weapon": "shotgun",
    "tier": 1,
    "requires": None,
    "tags": ["damage"],
    "base_weight": 3
},

"shotgun_knockback": {
    "name": "Heavy Knockback",
    "group": "weapon",
    "category": "damage",
    "weapon": "shotgun",
    "tier": 1,
    "requires": None,
    "tags": ["control"],
    "base_weight": 3
},

# SMG

"smg_overclock": {
    "name": "Overclock",
    "group": "weapon",
    "category": "damage",
    "weapon": "smg",
    "tier": 1,
    "requires": None,
    "tags": ["fire_rate"],
    "base_weight": 3
},

"smg_stream": {
    "name": "Bullet Stream",
    "group": "weapon",
    "category": "damage",
    "weapon": "smg",
    "tier": 1,
    "requires": None,
    "tags": ["damage"],
    "base_weight": 3
},

"smg_combo_boost": {
    "name": "Combo Boost",
    "group": "weapon",
    "category": "damage",
    "weapon": "smg",
    "tier": 1,
    "requires": None,
    "tags": ["combo"],
    "base_weight": 3
},

# LASER

"laser_cooldown": {
    "name": "Faster Charge",
    "group": "weapon",
    "category": "damage",
    "weapon": "laser",
    "tier": 1,
    "requires": None,
    "tags": ["fire_rate"],
    "base_weight": 3
},

"laser_pierce": {
    "name": "Piercing Beam",
    "group": "weapon",
    "category": "damage",
    "weapon": "laser",
    "tier": 1,
    "requires": None,
    "tags": ["damage"],
    "base_weight": 3
},

"laser_follow": {
    "name": "Follow Beam",
    "group": "weapon",
    "category": "damage",
    "weapon": "laser",
    "tier": 1,
    "requires": None,
    "tags": ["control"],
    "base_weight": 3
}

}