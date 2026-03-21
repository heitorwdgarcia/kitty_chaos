import pygame

from settings import *
from core import game_state as gs
from core.input_handler import handle_input
from core import game
from core.renderer import render

from systems.run_initializer import start_run

# UI (somente telas principais)
from ui import init_ui
from ui.main_menu import draw_main_menu
from ui.shop_menu import draw_shop
from ui.weapon_select import draw_weapon_select


pygame.init()
init_ui()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chaos Dodge")

clock = pygame.time.Clock()

running = True

# =========================================================
# MAIN LOOP
# =========================================================

while running:

    # -------------------------------------------------
    # CLOCK
    # -------------------------------------------------

    if gs.bot_mode:
        clock.tick(1200)
    else:
        clock.tick(60)

    # -------------------------------------------------
    # INPUT
    # -------------------------------------------------

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        handle_input(event, start_run)

    # -------------------------------------------------
    # UPDATE
    # -------------------------------------------------

    state = game.update(keys)

    # -------------------------------------------------
    # HIT STOP
    # -------------------------------------------------

    if state == "hit_stop":

        if gs.game_state == "run":
            render(screen)

        pygame.display.update()
        continue

    # -------------------------------------------------
    # RENDER
    # -------------------------------------------------

    if gs.game_state == "menu":
        draw_main_menu(screen)

    elif gs.game_state == "shop":
        draw_shop(screen)

    elif gs.game_state == "weapon_select":
        draw_weapon_select(screen)

    else:
        render(screen)

    pygame.display.update()


pygame.quit()