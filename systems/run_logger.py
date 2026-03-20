import json
from core import game_state as gs
import systems.run_director as run_director

FILE = r"C:\Users\heito\Documents\Programação\chaos_dodge - v2\telemetry_runs.jsonl"

run_data = None


# =========================================================
# START RUN
# =========================================================

def start_run():

    global run_data

    run_data = {

        # ---------------- RUN ----------------

        "run_time": 0,
        "death_reason": None,

        # ---------------- COMBAT ----------------

        "kills": 0,
        "shots_fired": 0,
        "shots_hit": 0,

        # ---------------- PLAYER ----------------

        "hits_taken": 0,
        "player_hp_lost": 0,

        # ---------------- DODGE ----------------

        "near_misses": 0,

        # ---------------- WORLD ----------------

        "world_damage_taken": 0,

        # ---------------- PICKUPS ----------------

        "ammo_collected": 0,
        "gems_collected": 0,

        # ---------------- WEAPON ----------------

        "weapon_start": gs.weapon,
        "weapon_final": None,

        # ---------------- UPGRADES ----------------

        "upgrades_taken": [],
        "upgrades_offered": [],

        # ---------------- SYSTEMS ----------------

        "rage_explosions": 0,
        "rage_kills": 0,

        # ---------------- EVENTS ----------------

        "miniboss_count": 0,
        "boss_reached": False,

        # ---------------- PROGRESSION ----------------

        "stage_reached": 0,
        "death_stage": 0,
        "death_event": None,

        "stage_time": [],
        "stage_kills": [],
        "spawn_pressure": []
    }


# =========================================================
# END RUN
# =========================================================

def end_run(reason):

    global run_data

    if run_data is None:
        return

    run_data["run_time"] = round(gs.run_timer / 60, 2)
    run_data["weapon_final"] = gs.weapon
    run_data["death_reason"] = reason

    # progressão da run
    run_data["stage_reached"] = run_director.current_index + 1
    run_data["death_stage"] = run_director.current_index

    if run_director.current_event:
        run_data["death_event"] = type(run_director.current_event).__name__

    try:

        with open(FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(run_data) + "\n")

    except Exception as e:
        print("Telemetry write error:", e)

    run_data = None


# =========================================================
# COMBAT
# =========================================================


def log_kill():

    if run_data:
        run_data["kills"] += 1

        stage = run_director.current_index

        while stage >= len(run_data["stage_kills"]):
            run_data["stage_kills"].append(0)

        run_data["stage_kills"][stage] += 1


def log_shot():

    if run_data:
        run_data["shots_fired"] += 1


def log_hit_enemy():

    if run_data:
        run_data["shots_hit"] += 1


# =========================================================
# PLAYER
# =========================================================

def log_player_hit():

    if run_data:
        run_data["hits_taken"] += 1


def log_player_hp_loss(amount):

    if run_data:
        run_data["player_hp_lost"] += amount


# =========================================================
# PICKUPS
# =========================================================

def log_ammo(amount):

    if run_data:
        run_data["ammo_collected"] += amount


def log_gem():

    if run_data:
        run_data["gems_collected"] += 1


# =========================================================
# DODGE
# =========================================================

def log_near_miss():

    if run_data:
        run_data["near_misses"] += 1


# =========================================================
# WORLD
# =========================================================

def log_world_damage(amount):

    if run_data:
        run_data["world_damage_taken"] += amount


# =========================================================
# UPGRADES
# =========================================================

def log_upgrade_offered(options):

    if run_data:
        run_data["upgrades_offered"].append(options)


def log_upgrade_taken(name):

    if run_data:

        run_data["upgrades_taken"].append({

            "name": name,
            "time": round(gs.run_timer / 60, 2),
            "kills_at_pick": gs.kills

        })


# =========================================================
# RAGE SYSTEM
# =========================================================

def log_rage_trigger():

    if run_data:
        run_data["rage_explosions"] += 1


def log_rage_kill():

    if run_data:
        run_data["rage_kills"] += 1


# =========================================================
# EVENTS
# =========================================================

def log_miniboss():

    if run_data:
        run_data["miniboss_count"] += 1


def log_boss():

    if run_data:
        run_data["boss_reached"] = True

# =========================================================
# STAGE SYSTEM
# =========================================================

def log_stage_start():

    if not run_data:
        return

    run_data["stage_time"].append(0)
    run_data["stage_kills"].append(0)
    run_data["spawn_pressure"].append(0)

# =========================================================
# STAGE TELEMETRY
# =========================================================

def log_stage_tick():

    if not run_data:
        return

    stage = run_director.current_index

    if stage < len(run_data["stage_time"]):

        run_data["stage_time"][stage] += 1

        # pressão de spawn = inimigos vivos
        pressure = len(gs.enemies)

        if gs.miniboss:
            pressure += 1

        if gs.boss:
            pressure += 1

        run_data["spawn_pressure"][stage] += pressure