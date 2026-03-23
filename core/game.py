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
from systems.feedback_system import process_feedback
from systems.run_state_controller import update_run_state
from systems.bot_manager import update_bot_manager
from systems.run_initializer import start_run
from systems.combat_system import update_combat
from systems.damage_system import process_damage
from systems.kill_system import process_kills
from systems.pickups import process_pickup_spawns


def update_run_flow(keys):

    if gs.reward_active:

        if gs.bot_mode:
            from systems.reward_system import choose_reward

            if gs.reward_choices:
                choose_reward(0)

        return True

    gs.run_timer += 1

    if gs.player_iframes > 0:
        gs.player_iframes -= 1

    if update_run_state():
        return True

    return False


def update_entities(keys):

    update_player()
    update_combat(keys)
    move_enemies()
    update_dodge()

    process_damage()
    process_kills()


def update_effects():

    # 🔥 ORDEM CRÍTICA (mantida)
    update_combo()
    process_pickup_spawns()
    update_particles()
    update_pickups()

    update_camera()
    process_feedback()

def update_world():

    update_run_director()
    update_boss()

    if gs.miniboss:
        gs.miniboss.update()

    update_world_integrity()


def update_run(keys):

    # 🔥 RESET ANTI-SPAM (ESSENCIAL)
    gs.ammo_spawned_this_frame = 0

    if update_run_flow(keys):
        return

    update_world()
    update_entities(keys)
    update_effects()


def update(keys):

    if gs.hit_stop > 0:
        gs.hit_stop -= 1
        return

    if gs.start_requested:
        gs.start_requested = False
        start_run()

    if gs.game_state == "run":
        update_run(keys)

    update_bot_manager(start_run)