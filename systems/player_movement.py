import pygame
from core import game_state as gs
from settings import *


def update_player():

    speed = PLAYER_SPEED * gs.move_speed_mult

    # -------------------------------------------------
    # PLAYER INPUT
    # -------------------------------------------------

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        gs.player_x -= speed

    if keys[pygame.K_RIGHT]:
        gs.player_x += speed

    # -------------------------------------------------
    # LIMITES DA TELA
    # -------------------------------------------------

    gs.player_x = max(0, min(WIDTH - PLAYER_W, gs.player_x))