class Particle:

    def __init__(self, x, y, vx, vy, life):

        self.x = x
        self.y = y

        self.vx = vx
        self.vy = vy

        self.life = life


    def update(self):

        self.x += self.vx
        self.y += self.vy

        self.life -= 1