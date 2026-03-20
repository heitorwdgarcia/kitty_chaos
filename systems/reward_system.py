from core import game_state as gs

from systems.apply_upgrade import apply_upgrade
from systems.upgrades_selector import generate_upgrade_choices

from systems.run_logger import (
    log_upgrade_offered,
    log_upgrade_taken
)


# =========================================================
# SPAWN CHEST
# =========================================================

def spawn_chest():

    gs.reward_active = True

    # usa novo selector inteligente
    gs.reward_choices = generate_upgrade_choices(gs)

    log_upgrade_offered(gs.reward_choices)


# =========================================================
# CHOOSE REWARD
# =========================================================

def choose_reward(index):

    upgrade = gs.reward_choices[index]

    apply_upgrade(gs, upgrade)

    gs.upgrades_taken.append(upgrade)

    log_upgrade_taken(upgrade)

    gs.reward_active = False