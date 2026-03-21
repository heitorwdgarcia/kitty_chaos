from core import game_state as gs

from systems.run_logger import end_run
from systems.nemesis_system import finalize_run
from systems.run_rewards import give_run_reward


def end_current_run(reason):

    give_run_reward()

    end_run(reason)

    finalize_run()

    gs.game_state = "result"