from pygame import Vector2

class Ant:
    def __init__(self, position: Vector2):
        self.pos = position
        self.life = 1

    def step(self):
        self.life -= 1