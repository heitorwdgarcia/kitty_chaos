class Bullet:

    def __init__(self, x, y, speed=10, damage=1, pierce=1):

        self.x = x
        self.y = y

        from core import game_state as gs
        self.speed = speed * gs.projectile_speed_mult
        
        self.damage = damage
        self.pierce = pierce


    def update(self):

        self.y -= self.speed