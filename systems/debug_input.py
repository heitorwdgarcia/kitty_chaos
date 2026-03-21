import pygame
from core import game_state as gs


def handle_debug_input(event, start_run):

    if event.type != pygame.KEYDOWN:
        return

    # -------------------------------------------------
    # BOT TYPE
    # -------------------------------------------------

    if event.key == pygame.K_F1:
        gs.bot_type = "beginner"

    elif event.key == pygame.K_F2:
        gs.bot_type = "intermediate"

    elif event.key == pygame.K_F3:
        gs.bot_type = "advanced"

    # -------------------------------------------------
    # BOT RUNS
    # -------------------------------------------------

    elif event.key == pygame.K_F9:

        if gs.bot_type:
            gs.bot_mode = True
            gs.bot_runs_remaining = 1
            start_run()

    elif event.key == pygame.K_F10:

        if gs.bot_type:
            gs.bot_mode = True
            gs.bot_runs_remaining = 10
            start_run()

    elif event.key == pygame.K_F11:

        if gs.bot_type:
            gs.bot_mode = True
            gs.bot_runs_remaining = 100
            start_run()