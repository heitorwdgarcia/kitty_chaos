from core import game_state as gs
# reward system
from meta.rewards import reward_gems
# =========================================================
# RUN REWARD
# =========================================================

def give_run_reward():

    gems = 1
    gems += gs.kills // 25

    reward_gems(gems)