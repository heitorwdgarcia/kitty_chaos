import random
from core import game_state as gs
from entities.particle import Particle

MAX_PARTICLES = 200


def spawn_hit_particles(x, y):

    if len(gs.particles) > MAX_PARTICLES:
        return

    for _ in range(8):

        gs.particles.append(
            Particle(
                x,
                y,
                random.uniform(-2, 2),
                random.uniform(-2, 2),
                random.randint(10, 20)
            )
        )


def update_particles():

    for p in gs.particles:
        p.update()

    gs.particles[:] = [p for p in gs.particles if p.life > 0]

    if len(gs.particles) > MAX_PARTICLES:
        gs.particles[:] = gs.particles[-MAX_PARTICLES:]