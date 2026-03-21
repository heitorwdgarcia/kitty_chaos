from core import game_state as gs
import pygame

from systems.debug_input import handle_debug_input

from ui.main_menu import update_menu_input
from ui.shop_menu import update_shop_input
from ui.weapon_select import update_weapon_select_input


def handle_input(event, start_run):

    if event.type != pygame.KEYDOWN:
        return

    # DEBUG (global)
    handle_debug_input(event, start_run)

    # -------------------------------------------------
    # REWARD
    # -------------------------------------------------

    if gs.reward_active:

        if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):

            from systems.reward_system import choose_reward

            index = event.key - pygame.K_1

            if index < len(gs.reward_choices):
                choose_reward(index)

        return

    # -------------------------------------------------
    # GAME STATES
    # -------------------------------------------------

    if gs.game_state == "menu":
        update_menu_input(event)

    elif gs.game_state == "shop":
        update_shop_input(event)

    elif gs.game_state == "weapon_select":
        update_weapon_select_input(event)

    elif gs.game_state == "result":

        if event.key == pygame.K_SPACE:
            gs.game_state = "menu"