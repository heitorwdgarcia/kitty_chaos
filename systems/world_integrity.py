from core import game_state as gs

def apply_world_damage(amount):

    if gs.world_shield:
        amount = max(0, amount - 1)

    gs.world_integrity -= amount
    
def update_world_integrity():

    # =================================================
    # WORLD REGEN
    # =================================================

    if gs.world_regen > 0 and gs.world_integrity < gs.max_world_integrity:

        gs.world_integrity += gs.world_regen


    # clamp valores
    gs.world_integrity = max(
        0,
        min(gs.world_integrity, gs.max_world_integrity)
    )


    # =================================================
    # WORLD CRITICAL ALERT
    # =================================================

    ratio = gs.world_integrity / gs.max_world_integrity

    if ratio < 0.30 and not hasattr(gs, "world_critical_warning"):

        gs.pending_feedback.append({
            "type": "world_critical",
            "x": 250,
            "y": 500
        })

        gs.world_critical_warning = True