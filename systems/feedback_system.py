from core import game_state as gs
from ui import spawn_message


def process_feedback():

    if not hasattr(gs, "pending_feedback"):
        return

    for e in gs.pending_feedback:

        etype = e.get("type")

        # ---------------- COMBO ----------------
        if etype == "combo":

            spawn_message(
                f"COMBO {e['value']}x",
                e["x"],
                e["y"],
                (255,255,120)
            )

        # ---------------- NEAR MISS ----------------
        elif etype == "near_miss":

            spawn_message(
                "NEAR MISS",
                e["x"],
                e["y"],
                (255,220,120)
            )

        # ---------------- WORLD CRITICAL ----------------
        elif etype == "world_critical":

            spawn_message(
                "WORLD CRITICAL",
                e["x"],
                e["y"],
                (255,80,80)
            )

        # ---------------- FX ----------------
        elif etype == "shake":

            gs.screen_shake = max(gs.screen_shake, e.get("duration", 5))
            gs.screen_shake_power = max(gs.screen_shake_power, e.get("power", 5))

        elif etype == "hit_stop":

            gs.hit_stop = min(
                max(gs.hit_stop, e.get("duration", 5)),
                20  # limite de segurança
            )

    gs.pending_feedback.clear()