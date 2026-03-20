import pygame

font = None


def init_ui():
    global font
    font = pygame.font.SysFont(None, 36)


def get_font():
    return font