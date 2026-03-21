from core import game_state as gs

from systems.run_events import (
    CombatEvent,
    EliteEvent,
    MinibossEvent,
    BossEvent
)

# =========================================================
# RUN STRUCTURE
# =========================================================

RUN_STRUCTURE = [

    # BLOCO 1
    {"type": "combat", "tier": "early", "mood": "breath", "duration": 15},
    {"type": "combat", "tier": "early", "mood": "intense", "duration": 15},
    {"type": "combat", "tier": "early", "mood": "chaos", "duration": 15},
    {"type": "miniboss","profile": "hunter"},

    # BLOCO 2
    {"type": "combat", "tier": "mid", "mood": "breath", "duration": 15},
    {"type": "combat", "tier": "mid", "mood": "intense", "duration": 15},
    {"type": "combat", "tier": "mid", "mood": "chaos", "duration": 15},
    {"type": "miniboss","profile": "hunter"},

    # BLOCO 3
    {"type": "combat", "tier": "late", "mood": "breath", "duration": 15},
    {"type": "combat", "tier": "late", "mood": "intense", "duration": 15},
    {"type": "combat", "tier": "late", "mood": "chaos", "duration": 15},
    {"type": "boss"},
]

# =========================================================
# GLOBAL STATE
# =========================================================

current_index = 0
current_event = None

current_intensity = 0.0
target_intensity = 0.0
stage_start_intensity = 0.0

stage_duration = 0
stage_timer = 0

current_tier = "early"


# =========================================================
# INTENSITY MODEL
# =========================================================

BASE_TIER = {
    "early": 0.35,
    "mid": 0.53,
    "late": 0.71
}

MOOD_OFFSET = {
    "breath": -0.10,
    "intense": 0.05,
    "chaos": 0.20
}


def compute_target_intensity(tier, mood):

    base = BASE_TIER.get(tier, 0.5)
    mood_offset = MOOD_OFFSET.get(mood, 0)

    intensity = base + mood_offset

    if intensity < 0.05:
        intensity = 0.05

    if intensity > 1.0:
        intensity = 1.0

    return intensity


# =========================================================
# START RUN
# =========================================================

def start_run():

    global current_index
    global current_event
    global current_intensity
    global current_tier
    global stage_timer

    current_index = 0
    current_intensity = 0.0
    current_tier = "early"
    stage_timer = 0

    load_event()


# =========================================================
# LOAD EVENT
# =========================================================

def load_event():

    global current_event
    global stage_start_intensity
    global target_intensity
    global stage_duration
    global current_tier
    global stage_timer

    stage_timer = 0

    data = RUN_STRUCTURE[current_index]

    t = data["type"]

    # -------------------------------------------------
    # COMBAT EVENT
    # -------------------------------------------------

    if t == "combat":

        duration = data["duration"]
        tier = data["tier"]
        mood = data["mood"]

        current_tier = tier

        stage_duration = duration * 60

        target_intensity = compute_target_intensity(tier, mood)

        stage_start_intensity = max(0.10, target_intensity - 0.15)

        current_event = CombatEvent(duration)

    elif t == "elite_enemy":

        current_event = EliteEvent()

    elif t == "miniboss":

        profile = data.get("profile")
        current_event = MinibossEvent(profile)

        reset_intensity()

    elif t == "boss":

        current_event = BossEvent()

        reset_intensity()

    from systems.run_logger import log_stage_start
    log_stage_start()


# =========================================================
# RESET INTENSITY
# =========================================================

def reset_intensity():

    global current_intensity

    current_intensity = 0.10


# =========================================================
# UPDATE INTENSITY
# =========================================================

def update_intensity():

    global current_intensity

    if stage_duration <= 0:
        return

    event = current_event

    if not isinstance(event, CombatEvent):
        return

    progress = event.timer / stage_duration
    progress = max(0, min(1, progress))

    curve = progress ** 1.4

    base_intensity = (

        stage_start_intensity +
        (target_intensity - stage_start_intensity) * curve

    )

    # -------------------------------------------------
    # AI DIRECTOR
    # -------------------------------------------------

    enemy_count = len(gs.enemies)

    if gs.miniboss:
        enemy_count += 1

    if gs.boss:
        enemy_count += 1

    target_enemies = 6 + base_intensity * 8

    pressure = enemy_count / max(1, target_enemies)

    pressure = max(0.5, min(1.5, pressure))

    current_intensity = base_intensity * (1 / pressure) ** 0.5


# =========================================================
# GETTERS
# =========================================================

def get_intensity():
    return current_intensity


def get_tier():
    return current_tier


# 🔥 NOVO — CONTEXTO CENTRALIZADO (INTEGRAÇÃO)
def get_run_context():

    return {
        "tier": current_tier,
        "intensity": current_intensity,
        "event_type": type(current_event).__name__ if current_event else None,
        "stage_progress": (
            current_event.timer / stage_duration
            if current_event and stage_duration > 0
            else 0
        )
    }


# =========================================================
# UPDATE DIRECTOR
# =========================================================

def update_run_director():
    from systems.run_logger import log_stage_tick
    log_stage_tick()

    global current_index
    global stage_timer

    if current_event is None:
        return

    stage_timer += 1

    update_intensity()

    finished = current_event.update()

    if finished:

        current_index += 1

        if current_index >= len(RUN_STRUCTURE):

            from systems.run_logger import end_run
            from systems.nemesis_system import finalize_run

            end_run("run_completed")
            finalize_run()

            gs.game_state = "result"

            return

        load_event()