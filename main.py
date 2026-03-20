import pygame

from settings import *
from core import game_state as gs

# systems
from systems.enemies import move_enemies
from systems.bullets import move_bullets
from systems.collisions import bullet_enemy_collision, player_enemy_collision
from systems.particles import update_particles
from systems.pickups import update_pickups
from systems.combo import update_combo
from systems.dodge import update_dodge
from systems.laser import update_laser
from systems.camera import update_camera, get_camera_offset
from systems.player_movement import update_player
from systems.player_combat import handle_shooting
from systems.boss_logic import update_boss
from systems.run_director import update_run_director
from systems.world_integrity import update_world_integrity
from systems.run_logger import start_run as telemetry_start_run, end_run
from systems.bot_manager import update_bot_manager

# reward system
from meta.rewards import reward_gems

# UI
from ui import init_ui, draw_ui, draw_entities, draw_messages
from ui.ui import get_font
from ui.main_menu import draw_main_menu, update_menu_input
from ui.shop_menu import draw_shop, update_shop_input
from ui.weapon_select import draw_weapon_select, update_weapon_select_input


pygame.init()
init_ui()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chaos Dodge")

clock = pygame.time.Clock()

running = True


# =========================================================
# START RUN
# =========================================================

def start_run():

    telemetry_start_run()

    from systems.nemesis_system import start_run as nemesis_start
    nemesis_start()

    import systems.run_director as run_director
    run_director.start_run()

    gs.run_timer = 0

    gs.kills = 0
    gs.chaos = 0
    gs.combo = 0
    gs.combo_timer = 0

    gs.enemies.clear()
    gs.bullets.clear()
    gs.particles.clear()
    gs.pickups.clear()

    gs.boss = None
    gs.miniboss = None

    gs.player_x = WIDTH // 2
    gs.player_y = HEIGHT - 120

    gs.player_hp = gs.player_max_hp
    gs.player_iframes = 0
    gs.ammo = max(1, gs.max_ammo)

    gs.fire_rate_mult = 1.0
    gs.double_shot = False
    gs.extra_pierce = 0

    gs.upgrades_taken = []

    gs.player_upgrades = []
    gs.build_tags = set()

    gs.rage_level = 0
    gs.rage_radius = 0
    gs.rage_damage = 0
    gs.rage_ammo = False
    gs.rage_chain = False

    gs.ammo_starve_timer = 0

    if hasattr(gs, "world_critical_warning"):
        del gs.world_critical_warning

    gs.spawn_timer = 0
    gs.shoot_timer = 0

    gs.world_integrity = gs.max_world_integrity

    gs.reward_active = False
    gs.reward_choices = []

    if gs.bot_mode:
        gs.weapon = "pistol"
        gs.game_state = "run"
    else:
        gs.game_state = "weapon_select"


# =========================================================
# RUN REWARD
# =========================================================

def give_run_reward():

    gems = 1
    gems += gs.kills // 25

    reward_gems(gems)


# =========================================================
# UPDATE GAME
# =========================================================

def update_game(keys):

    if gs.reward_active:
        return

    gs.run_timer += 1

    from systems.run_logger import log_stage_tick
    log_stage_tick()

    if gs.player_iframes > 0:
        gs.player_iframes -= 1

    update_run_director()

    update_boss()

    if gs.miniboss:
        gs.miniboss.update()

    update_world_integrity()

    update_player()
    handle_shooting(keys)

    update_laser()

    move_enemies()
    move_bullets()

    bullet_enemy_collision()

    if player_enemy_collision():

        give_run_reward()
        end_run("enemy_collision")

        from systems.nemesis_system import finalize_run
        finalize_run()

        gs.game_state = "result"
        return

    update_dodge()

    if gs.world_integrity <= 0:

        give_run_reward()
        end_run("world_destroyed")

        from systems.nemesis_system import finalize_run
        finalize_run()

        gs.game_state = "result"
        return

    update_combo()

    update_particles()
    update_pickups()

    update_camera()


# =========================================================
# RENDER GAME
# =========================================================

def render_game():

    shake_x, shake_y = get_camera_offset()

    screen.fill((15, 15, 20))

    draw_entities(screen, shake_x, shake_y)

    draw_messages(screen)

    draw_ui(screen)


# =========================================================
# RESULT SCREEN
# =========================================================

def render_result():

    screen.fill((10,10,15))

    font = get_font()

    text = font.render("RUN OVER", True, (255,255,255))
    kills = font.render(f"KILLS: {gs.kills}", True, (200,200,200))
    restart = font.render("PRESS SPACE", True, (160,160,160))

    screen.blit(text, (WIDTH//2 - text.get_width()//2, 250))
    screen.blit(kills, (WIDTH//2 - kills.get_width()//2, 300))
    screen.blit(restart, (WIDTH//2 - restart.get_width()//2, 350))


# =========================================================
# MAIN LOOP
# =========================================================

while running:

    if gs.bot_mode:
        clock.tick(1200)
    else:
        clock.tick(60)

    keys = pygame.key.get_pressed()

    if gs.reward_active and gs.bot_mode:

        from systems.reward_system import choose_reward

        if gs.reward_choices:
            choose_reward(0)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:

            # -------------------------------------------------
            # ESCOLHER BOT
            # -------------------------------------------------

            if event.key == pygame.K_F1:
                gs.bot_type = "beginner"

            if event.key == pygame.K_F2:
                gs.bot_type = "intermediate"

            if event.key == pygame.K_F3:
                gs.bot_type = "advanced"

            # -------------------------------------------------
            # ESCOLHER QUANTIDADE DE RUNS
            # -------------------------------------------------

            if event.key == pygame.K_F9:

                if gs.bot_type:
                    gs.bot_mode = True
                    gs.bot_runs_remaining = 1
                    start_run()

            if event.key == pygame.K_F10:

                if gs.bot_type:
                    gs.bot_mode = True
                    gs.bot_runs_remaining = 10
                    start_run()

            if event.key == pygame.K_F11:

                if gs.bot_type:
                    gs.bot_mode = True
                    gs.bot_runs_remaining = 100
                    start_run()

            if gs.reward_active:

                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):

                    from systems.reward_system import choose_reward

                    index = event.key - pygame.K_1

                    if index < len(gs.reward_choices):
                        choose_reward(index)

            elif gs.game_state == "menu":
                update_menu_input(event)

            elif gs.game_state == "shop":
                update_shop_input(event)

            elif gs.game_state == "weapon_select":
                update_weapon_select_input(event)

            elif gs.game_state == "result":

                if event.key == pygame.K_SPACE:
                    gs.game_state = "menu"

    if gs.start_requested:

        gs.start_requested = False
        start_run()

    if gs.hit_stop > 0:

        gs.hit_stop -= 1

        if gs.game_state == "run":
            render_game()

        pygame.display.update()
        continue

    # UPDATE

    if gs.game_state == "run":
        update_game(keys)

    update_bot_manager(start_run)

    # RENDER

    if gs.game_state == "menu":
        draw_main_menu(screen)

    elif gs.game_state == "shop":
        draw_shop(screen)

    elif gs.game_state == "weapon_select":
        draw_weapon_select(screen)

    elif gs.game_state == "run":
        render_game()

    elif gs.game_state == "result":
        render_result()

    pygame.display.update()


pygame.quit()