import pygame

from core import game_state as gs
from ui.ui import get_font
from meta.shop import get_unlocked_weapons


selected = 0


def update_weapon_select_input(event):

    global selected

    weapons = get_unlocked_weapons()

    if event.key == pygame.K_UP:
        selected = max(0, selected - 1)

    elif event.key == pygame.K_DOWN:
        selected = min(len(weapons) - 1, selected + 1)

    elif event.key == pygame.K_RETURN:

        weapon = weapons[selected]

        gs.weapon = weapon

        gs.game_state = "run"


def draw_weapon_select(screen):

    screen.fill((10, 10, 15))

    font = get_font()

    title = font.render("CHOOSE WEAPON", True, (255,255,255))

    screen.blit(title, (200,150))

    weapons = get_unlocked_weapons()

    y = 260

    for i, weapon in enumerate(weapons):

        color = (200,200,200)

        if i == selected:
            color = (255,255,120)

        text = weapon.upper()

        surf = font.render(text, True, color)

        screen.blit(surf, (260, y))

        y += 50