import random
from core import game_state as gs


class Pickup:

    def __init__(self, x, y, kind="ammo"):

        self.x = x
        self.y = y

        self.kind = kind

        # -----------------------------
        # lifespan (upgrade support)
        # -----------------------------

        life_mult = getattr(gs, "pickup_lifespan_mult", 1.0)
        self.life = int(300 * life_mult)

        # -----------------------------
        # physics
        # -----------------------------

        self.vx = random.uniform(-1.2, 1.2)
        self.vy = random.uniform(-2.2, -1.2)

        self.gravity = 0.10


    def update(self):

        # movement
        self.x += self.vx
        self.y += self.vy

        # gravity
        self.vy += self.gravity

        # horizontal drag
        self.vx *= 0.98

        self.life -= 1