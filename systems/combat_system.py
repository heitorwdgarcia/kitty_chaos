from systems.player_combat import handle_shooting
from systems.bullets import move_bullets
from systems.collisions import bullet_enemy_collision
from systems.laser import update_laser

# =========================================================
# COMBAT UPDATE
# =========================================================

def update_combat(keys):

    # shooting
    handle_shooting(keys)

    # laser (agora faz parte do combate)
    update_laser()

    # bullets
    move_bullets()

    # collisions
    bullet_enemy_collision()