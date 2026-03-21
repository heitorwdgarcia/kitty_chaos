from core import game_state as gs

# systems
from systems.enemies import move_enemies
from systems.bullets import move_bullets
from systems.collisions import bullet_enemy_collision
from systems.particles import update_particles
from systems.pickups import update_pickups
from systems.combo import update_combo
from systems.dodge import update_dodge
from systems.laser import update_laser
from systems.camera import update_camera
from systems.player_movement import update_player
from systems.player_combat import handle_shooting
from systems.boss_logic import update_boss
from systems.run_director import update_run_director
from systems.world_integrity import update_world_integrity
from systems.run_state_controller import update_run_state
from systems.bot_manager import update_bot_manager
from systems.run_initializer import start_run
from systems.combat_system import update_combat




def update_run_flow(keys):

    # trava durante reward
    if gs.reward_active:

        # BOT AUTO PICK
        if gs.bot_mode:

            from systems.reward_system import choose_reward

            if gs.reward_choices:
                choose_reward(0)

        return True

    # timer
    gs.run_timer += 1

    # i-frames
    if gs.player_iframes > 0:
        gs.player_iframes -= 1

    # estado da run (morte etc)
    if update_run_state():
        return True

    return False

def update_entities(keys):

    # player
    update_player()

    # combate
    update_combat(keys)

    # entidades
    move_enemies()

    # dodge
    update_dodge()


def update_effects():

    # sistemas secundários
    update_combo()
    update_particles()
    update_pickups()

    # câmera
    update_camera()

# =========================================================
# UPDATE WORLD
# =========================================================

def update_world():

    # director
    update_run_director()

    # bosses
    update_boss()

    if gs.miniboss:
        gs.miniboss.update()

    # mundo
    update_world_integrity()


# =========================================================
# UPDATE RUN
# =========================================================

def update_run(keys):

    if update_run_flow(keys):
        return

    update_world()
    update_entities(keys)
    update_effects()


# =========================================================
# UPDATE (ENTRY POINT)
# =========================================================

def update(keys):

    # HIT STOP
    if gs.hit_stop > 0:
        gs.hit_stop -= 1
        return "hit_stop"

    # start run request
    if gs.start_requested:
        gs.start_requested = False

        from systems.run_initializer import start_run
        start_run()

    if gs.game_state == "run":
        update_run(keys)

    # BOT MANAGER (fora da run)
    update_bot_manager(start_run)