import pygame

from ui.ui import get_font
from core import game_state as gs


selected = 0

options = [
    "START RUN",
    "SHOP",
    "QUIT"
]


def update_menu_input(event):

    global selected

    if event.key == pygame.K_UP:
        selected = max(0, selected-1)

    elif event.key == pygame.K_DOWN:
        selected = min(len(options)-1, selected+1)

    elif event.key == pygame.K_RETURN:

        if options[selected] == "START RUN":
            gs.start_requested = True

        elif options[selected] == "SHOP":
            gs.game_state = "shop"

        elif options[selected] == "QUIT":
            pygame.quit()
            exit()


def draw_main_menu(screen):

    font = get_font()

    screen.fill((10,10,15))

    title = font.render("CHAOS DODGE", True, (255,255,255))

    screen.blit(title, (200,120))

    # -------------------------------------------------
    # BOT DEBUG INFO
    # -------------------------------------------------
    font_small = get_font()

    y_bot = 420

    screen.blit(
        font_small.render("BOT TEST MODE", True, (120,200,255)),
        (20, y_bot)
    )

    y_bot += 30

    screen.blit(
        font_small.render("F1 Beginner", True, (200,200,200)),
        (20, y_bot)
    )

    y_bot += 25

    screen.blit(
        font_small.render("F2 Intermediate", True, (200,200,200)),
        (20, y_bot)
    )

    y_bot += 25

    screen.blit(
        font_small.render("F3 Advanced", True, (200,200,200)),
        (20, y_bot)
    )

    y_bot += 30

    screen.blit(
        font_small.render("F9  → 1 Run", True, (200,200,200)),
        (20, y_bot)
    )

    y_bot += 25

    screen.blit(
        font_small.render("F10 → 10 Runs", True, (200,200,200)),
        (20, y_bot)
    )

    y_bot += 25

    screen.blit(
        font_small.render("F11 → 100 Runs", True, (200,200,200)),
        (20, y_bot)
    )

    y_bot += 30

    bot_name = getattr(gs, "bot_type", None)

    if bot_name:
        text = f"CURRENT BOT: {bot_name.upper()}"
    else:
        text = "CURRENT BOT: NONE"

    screen.blit(
        font_small.render(text, True, (255,255,120)),
        (20, y_bot)
    )



    y = 260

    for i, option in enumerate(options):

        color = (200,200,200)

        if i == selected:
            color = (255,255,120)

        surf = font.render(option, True, color)

        screen.blit(surf, (240,y))

        y += 60