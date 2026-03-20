import random
import pygame
from core import game_state as gs
from .ui import get_font


def spawn_message(text, x, y, color):

    # -------------------------------------------------
    # COMBO MESSAGE UPDATE (não criar várias)
    # -------------------------------------------------

    if text.startswith("COMBO"):

        for msg in gs.messages:

            if msg[0].startswith("COMBO"):

                msg[0] = text
                msg[1] = 60
                return

    # -------------------------------------------------
    # NOVA MENSAGEM
    # -------------------------------------------------

    offset_x = random.randint(-20, 20)

    stack_offset = len(gs.messages) * 18

    gs.messages.append([
        text,                # 0 text
        60,                  # 1 life
        x + offset_x,        # 2 x
        y - stack_offset,    # 3 y
        color                # 4 color
    ])


def draw_messages(screen):

    font = get_font()

    for msg in gs.messages[:]:

        text = msg[0]
        life = msg[1]
        x = msg[2]
        y = msg[3]
        color = msg[4]

        surf = font.render(text, True, color)

        # -------------------------------------------------
        # FADE
        # -------------------------------------------------

        alpha = int(255 * (life / 60))
        surf.set_alpha(alpha)

        screen.blit(surf, (x, y))

        # -------------------------------------------------
        # ANIMAÇÃO
        # -------------------------------------------------

        msg[1] -= 1
        msg[3] -= 0.4

        if msg[1] <= 0:
            gs.messages.remove(msg)