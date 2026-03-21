from core import game_state as gs
from systems.run_logger import start_run as telemetry_start_run, end_run
from settings import WIDTH, HEIGHT
# =========================================================
# START RUN
# =========================================================

def start_run():

    telemetry_start_run()

    from systems.nemesis_system import start_run as nemesis_start
    nemesis_start()

    import systems.run_director as run_director
    run_director.start_run()

    gs.run_timer = 0

    gs.kills = 0
    gs.chaos = 0
    gs.combo = 0
    gs.combo_timer = 0

    gs.enemies.clear()
    gs.bullets.clear()
    gs.particles.clear()
    gs.pickups.clear()

    gs.boss = None
    gs.miniboss = None

    gs.player_x = WIDTH // 2
    gs.player_y = HEIGHT - 120

    gs.player_hp = gs.player_max_hp
    gs.player_iframes = 0
    gs.ammo = max(1, gs.max_ammo)

    gs.fire_rate_mult = 1.0
    gs.double_shot = False
    gs.extra_pierce = 0

    gs.upgrades_taken = []

    gs.player_upgrades = []
    gs.build_tags = set()

    gs.rage_level = 0
    gs.rage_radius = 0
    gs.rage_damage = 0
    gs.rage_ammo = False
    gs.rage_chain = False

    gs.ammo_starve_timer = 0

    if hasattr(gs, "world_critical_warning"):
        del gs.world_critical_warning

    gs.spawn_timer = 0
    gs.shoot_timer = 0

    gs.world_integrity = gs.max_world_integrity

    gs.reward_active = False
    gs.reward_choices = []

    if gs.bot_mode:
        gs.weapon = "pistol"
        gs.game_state = "run"
    else:
        gs.game_state = "weapon_select"