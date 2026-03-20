import pygame
from core import game_state as gs
from .ui import get_font
from settings import *

import systems.run_director as run_director


def draw_ui(screen):

    font = get_font()

    # -------------------------------------------------
    # PLAYER INFO
    # -------------------------------------------------

    screen.blit(
        font.render(f"Kills: {gs.kills}", True, (255,255,255)),
        (10,10)
    )

    screen.blit(
        font.render(f"Ammo: {gs.ammo}/{gs.max_ammo}", True, (255,255,255)),
        (10,40)
    )

    screen.blit(
        font.render(f"Weapon: {gs.weapon}", True, (255,255,255)),
        (10,70)
    )

    screen.blit(
        font.render(f"HP: {gs.player_hp}", True, (255,120,120)),
        (10,100)
    )

    # -------------------------------------------------
    # RUN TIMER
    # -------------------------------------------------

    minutes = gs.run_timer // 3600
    seconds = (gs.run_timer % 3600) // 60

    timer_text = f"{minutes}:{seconds:02d}"

    timer_surface = font.render(timer_text, True, (255,255,255))

    screen.blit(
        timer_surface,
        (WIDTH//2 - timer_surface.get_width()//2, 10)
    )


    # -------------------------------------------------
    # STAGE
    # -------------------------------------------------

    phase_surface = font.render(
        f"Stage {run_director.current_index + 1}",
        True,
        (180,180,180)
    )

    screen.blit(
        phase_surface,
        (WIDTH//2 - phase_surface.get_width()//2, 40)
    )


    # -------------------------------------------------
    # INTENSITY DEBUG
    # -------------------------------------------------

    intensity = run_director.get_intensity()

    intensity_text = font.render(
        f"Intensity: {int(intensity*100)}%",
        True,
        (200,200,120)
    )

    screen.blit(intensity_text, (10,130))


    # -------------------------------------------------
    # BOT MODE INFO
    # -------------------------------------------------

    if gs.bot_mode:

        bot_text = font.render(
            f"BOT RUNS LEFT: {gs.bot_runs_remaining}",
            True,
            (120,200,255)
        )

        screen.blit(
            bot_text,
            (WIDTH - bot_text.get_width() - 20, 10)
        )


    # -------------------------------------------------
    # BOSS HP BAR
    # -------------------------------------------------

    if gs.boss:

        bar_w = 320
        bar_h = 18

        x = WIDTH // 2 - bar_w // 2
        y = 70

        ratio = gs.boss.hp / gs.boss.max_hp if gs.boss.max_hp else 0
        ratio = max(0, min(1, ratio))

        pygame.draw.rect(screen, (60,0,0), (x,y,bar_w,bar_h))
        pygame.draw.rect(screen, (255,60,60), (x,y,int(bar_w*ratio),bar_h))
        pygame.draw.rect(screen, (255,255,255), (x,y,bar_w,bar_h), 2)


    # -------------------------------------------------
    # WORLD INTEGRITY BAR
    # -------------------------------------------------

    bar_w = 200
    bar_h = 14

    x = WIDTH - bar_w - 20
    y = HEIGHT - 40

    ratio = max(
        0,
        min(1, gs.world_integrity / gs.max_world_integrity)
    )

    pygame.draw.rect(screen, (40,40,40), (x,y,bar_w,bar_h))
    pygame.draw.rect(screen, (80,220,120), (x,y,int(bar_w * ratio),bar_h))
    pygame.draw.rect(screen, (255,255,255), (x,y,bar_w,bar_h), 2)

    label = font.render("WORLD", True, (255,255,255))

    screen.blit(label, (x - label.get_width() - 10, y - 4))


    # -------------------------------------------------
    # REWARD SCREEN
    # -------------------------------------------------

    if gs.reward_active:

        big_font = pygame.font.SysFont(None, 42)

        title = big_font.render("CHOOSE UPGRADE", True, (255,255,255))

        screen.blit(
            title,
            (WIDTH//2 - title.get_width()//2, 200)
        )

        y = 300

        for i, upgrade in enumerate(gs.reward_choices):

            text = f"{i+1} - {format_upgrade(upgrade)}"

            surf = font.render(text, True, (255,255,120))

            screen.blit(
                surf,
                (WIDTH//2 - surf.get_width()//2, y)
            )

            y += 50

        info = font.render("PRESS 1 / 2 / 3", True, (200,200,200))

        screen.blit(
            info,
            (WIDTH//2 - info.get_width()//2, y + 20)
        )


# -------------------------------------------------
# FORMAT UPGRADE TEXT
# -------------------------------------------------

def format_upgrade(up):

    names = {

        "fire_rate": "Faster Fire Rate",

        "double_shot": "Double Shot",

        "pierce": "Bullet Pierce",

        "ammo_cap": "Increase Ammo",

        "hp": "Extra HP"

    }

    return names.get(up, up)