import pygame

from ui.ui import get_font
from meta.shop import (
    WEAPON_ITEMS,
    UPGRADE_ITEMS,
    buy_weapon,
    buy_upgrade,
    get_player_gems,
    get_unlocked_weapons,
    get_unlocked_upgrades
)

from core import game_state as gs


selected_index = 0


def update_shop_input(event):

    global selected_index

    items = list(WEAPON_ITEMS.keys()) + list(UPGRADE_ITEMS.keys())

    if event.key == pygame.K_UP:
        selected_index = max(0, selected_index - 1)

    elif event.key == pygame.K_DOWN:
        selected_index = min(len(items)-1, selected_index + 1)

    elif event.key == pygame.K_RETURN:

        item = items[selected_index]

        if item in WEAPON_ITEMS:
            buy_weapon(item)

        elif item in UPGRADE_ITEMS:
            buy_upgrade(item)

    elif event.key == pygame.K_ESCAPE:

        gs.game_state = "menu"


def draw_shop(screen):

    font = get_font()

    screen.fill((10,10,15))

    title = font.render("SHOP", True, (255,255,255))
    screen.blit(title, (260,100))

    gems = get_player_gems()
    gem_text = font.render(f"GEMS: {gems}", True, (180,180,255))
    screen.blit(gem_text, (250,140))

    unlocked_weapons = get_unlocked_weapons()
    unlocked_upgrades = get_unlocked_upgrades()

    items = list(WEAPON_ITEMS.items()) + list(UPGRADE_ITEMS.items())

    y = 220

    for i, (item, price) in enumerate(items):

        color = (200,200,200)

        if i == selected_index:
            color = (255,255,120)

        text = f"{item.upper()} - {price} gems"

        if item in unlocked_weapons or item in unlocked_upgrades:
            text += " (OWNED)"

        surf = font.render(text, True, color)

        screen.blit(surf, (160,y))

        y += 40

    info = font.render("ENTER BUY | ESC BACK", True, (150,150,150))
    screen.blit(info, (170, y + 20))