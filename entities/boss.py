import random
import math


class Boss:

    def __init__(self, x, y, hp):

        self.x = x
        self.y = y

        self.max_hp = hp
        self.hp = hp

        #entity system
        self.is_hostile = True
        self.entity_type = "boss"

        self.timer = 0
        self.hit_timer = 0

        self.phase = random.random() * 10

        self.width = 80
        self.height = 60


    def update(self):

        self.timer += 1

        if self.y < 80:
            self.y += 2

        self.phase += 0.04
        self.x += math.sin(self.phase) * 2.5

        if self.x < 0:
            self.x = 0

        if self.x > 600 - self.width:
            self.x = 600 - self.width

        if self.hit_timer > 0:
            self.hit_timer -= 1