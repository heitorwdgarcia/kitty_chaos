from core import game_state as gs
from systems.kill_system import request_kill
from systems.run_logger import log_hit_enemy

# =========================================================
# REQUEST
# =========================================================

def request_damage(target, amount, source=None, damage_type="generic"):

    if not hasattr(gs, "pending_damage"):
        gs.pending_damage = []

    gs.pending_damage.append({
        "target": target,
        "amount": amount,
        "source": source,
        "damage_type": damage_type  # ✅ NOVO
    })


# =========================================================
# PROCESS
# =========================================================

def process_damage():

    if not hasattr(gs, "pending_damage"):
        return

    for d in gs.pending_damage:

        target = d["target"]
        amount = d["amount"]
        source = d["source"]
        damage_type = d.get("damage_type", "generic")  # ✅ NOVO

        # alvo inválido
        if target is None:
            continue

        # =================================================
        # PLAYER DAMAGE
        # =================================================

        if target == "player":

            # iframe
            if gs.player_iframes > 0:
                continue

            from systems.run_logger import log_player_hit, log_player_hp_loss

            log_player_hp_loss(amount)

            gs.player_hp -= amount

            # clamp segurança
            if gs.player_hp < 0:
                gs.player_hp = 0

            # efeitos on hit
            if gs.ammo_on_damage:
                gs.ammo = min(gs.ammo + 2, gs.max_ammo)

            # ativa iframe
            gs.player_iframes = gs.player_iframe_duration

            # morte do player
            if gs.player_hp <= 0:
                from systems.run_director import request_end_run
                request_end_run("player_damage")

            continue

        # =================================================
        # ENEMY DAMAGE
        # =================================================

        # já morreu → ignora
        if getattr(target, "is_dead", False):
            continue

        if hasattr(target, "hp"):
            if damage_type == "execution":
                target.hp = 0
            else:
                target.hp -= amount

            on_hit(target, amount, source, damage_type)  # ✅ ALTERADO

            # clamp segurança
            if target.hp < 0:
                target.hp = 0

            # -------------------------------------------------
            # REQUEST KILL (AUTORIDADE)
            # -------------------------------------------------

            if target.hp <= 0:
                request_kill(target, source=source)

    # limpa fila
    gs.pending_damage.clear()


# =========================================================
# HIT EVENT
# =========================================================

def on_hit(target, amount, source, damage_type):  # ✅ ALTERADO

    from core import game_state as gs

    # ---------------------------------
    # PLAYER HIT
    # ---------------------------------
    if target == "player":
        return

    # ---------------------------------
    # ENEMY HIT
    # ---------------------------------

    log_hit_enemy()

    # 🔥 FUTURO:
    # if damage_type == "crit":
    #     spawn_crit_effect()

    # spawn_hit_particles(target.x, target.y)