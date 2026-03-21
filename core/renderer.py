import pygame

from core import game_state as gs
from settings import *

from ui import draw_ui, draw_entities, draw_messages
from ui.ui import get_font

from systems.camera import get_camera_offset


# =========================================================
# RENDER GAME
# =========================================================

def render_game(screen):

    shake_x, shake_y = get_camera_offset()

    screen.fill((15, 15, 20))

    draw_entities(screen, shake_x, shake_y)
    draw_messages(screen)
    draw_ui(screen)


# =========================================================
# RESULT SCREEN
# =========================================================

def render_result(screen):

    screen.fill((10,10,15))

    font = get_font()

    text = font.render("RUN OVER", True, (255,255,255))
    kills = font.render(f"KILLS: {gs.kills}", True, (200,200,200))
    restart = font.render("PRESS SPACE", True, (160,160,160))

    screen.blit(text, (WIDTH//2 - text.get_width()//2, 250))
    screen.blit(kills, (WIDTH//2 - kills.get_width()//2, 300))
    screen.blit(restart, (WIDTH//2 - restart.get_width()//2, 350))


# =========================================================
# MASTER RENDER
# =========================================================

def render(screen):

    if gs.game_state == "run":
        render_game(screen)

    elif gs.game_state == "result":
        render_result(screen)