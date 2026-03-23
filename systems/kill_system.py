from core import game_state as gs

from systems.drop_system import enemy_drop
from systems.particles import spawn_hit_particles
from systems.run_logger import log_kill, log_rage_kill
from systems.combo import combo_reward
from systems.reward_system import spawn_chest

# =========================================================
# REQUEST
# =========================================================

def request_kill(enemy, source="unknown"):

    if not hasattr(gs, "pending_kills"):
        gs.pending_kills = []

    gs.pending_kills.append({
        "enemy": enemy,
        "source": source
    })


# =========================================================
# PROCESS
# =========================================================

def process_kills():

    if not hasattr(gs, "pending_kills"):
        return

    for k in gs.pending_kills:

        enemy = k["enemy"]
        source = k["source"]

        # evitar double kill
        if getattr(enemy, "is_dead", False):
            continue

        handle_death(enemy, source)

    gs.pending_kills.clear()


# =========================================================
# REMOVE (AUTORIDADE CENTRAL)
# =========================================================

def remove_enemy(enemy):

    # enemy normal
    if enemy in gs.enemies:
        gs.enemies.remove(enemy)
        return

    # miniboss
    if gs.miniboss is enemy:

        from systems.nemesis_system import record_fight

        stats = enemy.get_fight_stats()
        record_fight(enemy.profile, stats)

        gs.miniboss = None
        return

    # boss
    if gs.boss is enemy:
        gs.boss = None
        return


# =========================================================
# PIPELINE CENTRAL
# =========================================================

def handle_death(enemy, source):

    enemy.is_dead = True
    # -------------------------------------------------
    # POSIÇÃO
    # -------------------------------------------------

    cx = enemy.x + 20
    cy = enemy.y + 20

    # -------------------------------------------------
    # DROP
    # -------------------------------------------------

    enemy_drop(enemy)

    # -------------------------------------------------
    # GOLDEN REWARD
    # -------------------------------------------------

    if getattr(enemy, "is_golden", False):
        spawn_chest()

    # -------------------------------------------------
    # FX
    # -------------------------------------------------

    spawn_hit_particles(cx, cy)

    # -------------------------------------------------
    # STATS
    # -------------------------------------------------

    gs.kills += 1
    log_kill()

    # -------------------------------------------------
    # RAGE TELEMETRY (CENTRALIZADO)
    # -------------------------------------------------

    if source == "rage":
        
        log_rage_kill()

    # -------------------------------------------------
    # CHAOS
    # -------------------------------------------------

    gs.chaos += 0.3

    # -------------------------------------------------
    # COMBO
    # -------------------------------------------------

    gs.combo += 1
    gs.combo_timer = int(60 * gs.combo_duration_mult)

    if gs.combo >= 2:

        gs.pending_feedback.append({
            "type": "combo",
            "value": gs.combo,
            "x": cx,
            "y": cy
        })
    combo_reward()

    # -------------------------------------------------
    # REMOVE (SEMPRE ÚLTIMO)
    # -------------------------------------------------

    remove_enemy(enemy)