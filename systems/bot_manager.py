from core import game_state as gs

from systems.bots import (
    bot_beginner,
    bot_intermediate,
    bot_advanced
)

def update_bot_manager(start_run):

    if not gs.bot_mode:
        return

    # BOT DURANTE RUN
    if gs.game_state == "run":

        if gs.bot_type == "beginner":
            bot_beginner.update()

        elif gs.bot_type == "intermediate":
            bot_intermediate.update()

        elif gs.bot_type == "advanced":
            bot_advanced.update()

    # FIM DA RUN
    elif gs.game_state == "result":

        gs.bot_runs_remaining -= 1
        gs.bot_shoot = False

        if gs.bot_runs_remaining > 0:

            start_run()

        else:

            gs.bot_mode = False
            gs.bot_type = None
            gs.game_state = "menu"