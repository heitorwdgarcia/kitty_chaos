class World:

    def __init__(self):

        # ---------------- GAME STATE ----------------

        self.game_state = "menu"
        self.start_requested = False
        self.run_timer = 0

        # ---------------- DIRECTOR FLAGS ----------------

        self.final_boss_spawned = False
        self.miniboss_count = 0

        # ---------------- PLAYER ----------------

        self.player_x = 300
        self.player_y = 620

        # ---------------- ENTITIES ----------------

        self.enemies = []
        self.bullets = []
        self.particles = []
        self.pickups = []

        # ---------------- WEAPON ----------------

        self.weapon = "pistol"

        # ---------------- AMMO ----------------

        self.ammo = 5
        self.max_ammo = 5

        # ---------------- STATS ----------------

        self.kills = 0
        self.chaos = 0

        self.combo = 0
        self.combo_timer = 0

        # ---------------- WORLD ----------------

        self.world_integrity = 200
        self.max_world_integrity = 200
        self.world_leak_counter = 0

        # ---------------- BOSS ----------------

        self.boss = None

        # ---------------- MINIBOSS ----------------

        self.miniboss = None

        # ---------------- TIMERS ----------------

        self.shoot_timer = 0

        # ---------------- FX ----------------

        self.screen_shake = 0
        self.screen_shake_power = 0

        self.camera_x = 0
        self.camera_y = 0

        self.hit_stop = 0
        self.flash = 0

        # ---------------- LASER ----------------

        self.laser_active = False
        self.laser_timer = 0

        self.laser_charging = False
        self.laser_charge_timer = 0

        self.laser_x = 0
        self.laser_length = 0

        # ---------------- CORE COMBAT MODIFIERS ----------------

        self.fire_rate_mult = 1.0
        self.double_shot = False
        self.extra_pierce = 0

        self.bullet_damage_mult = 1.0
        self.projectile_speed_mult = 1.0

        self.knockback = 0
        self.ricochet = 0

        # ---------------- AMMO SYSTEM ----------------

        self.ammo_drop_bonus = 0
        self.near_miss_ammo = False
        self.near_miss_slow = False
        self.ammo_on_damage = False

        # ---------------- PICKUP SYSTEM ----------------

        self.pickup_lifespan_mult = 1.0
        self.pickup_size_mult = 1.0
        self.pickup_magnet_radius = 0

        self.double_pickups = False

        # ---------------- PLAYER MODIFIERS ----------------

        self.move_speed_mult = 1.0
        self.combo_duration_mult = 1.0

        self.small_hitbox = False
        self.second_chance = False
        self.ghost_dash = False

        # ---------------- COMBO UPGRADES ----------------

        self.combo_fire_rate = False
        self.combo_damage = False
        self.combo_ammo = False

        # ---------------- ECONOMY ----------------

        self.gem_value_mult = 1.0
        self.double_gems = False

        # ---------------- WORLD UPGRADES ----------------

        self.world_regen = 0
        self.world_shield = False

        # ---------------- WEAPON MODIFIERS ----------------

        # shotgun
        self.shotgun_spread = 0
        self.shotgun_double = False
        self.shotgun_knockback = 0

        # smg
        self.smg_extra_bullets = 0
        self.combo_boost = False

        # laser
        self.laser_cooldown_mult = 1.0
        self.laser_pierce = 0
        self.laser_follow = False

        # ---------------- BUILD SYSTEM ----------------

        self.player_upgrades = []
        self.build_tags = set()

        # ---------------- RAGE SYSTEM ----------------

        self.rage_level = 0
        self.rage_radius = 0
        self.rage_damage = 0

        self.rage_core = False
        self.rage_ammo = False
        self.rage_chain = False

        self.near_miss_radius = 60

        # ---------------- UI ----------------

        self.messages = []

        # ---------------- PLAYER STATS ----------------

        self.player_hp = 5
        self.player_max_hp = 5

        self.player_iframes = 0
        self.player_iframe_duration = 50

        # ---------------- REWARD ----------------

        self.reward_active = False
        self.reward_choices = []

        # ---------------- SAFETY ----------------

        self.ammo_starve_timer = 0

        # ---------------- RUN PROGRESSION ----------------

        self.kill_reward_index = 0
        self.next_kill_reward = 5

        # ---------------- BOT ----------------

        self.bot_mode = False
        self.bot_runs_remaining = 0
        self.bot_shoot = False

        # ---------------- VALORES UTEIS ----------------
        
        self.pickup_lifespan_mult = 1.0
        self.pickup_size_mult = 1.0
        self.double_pickups = False
        self.world_shield = False