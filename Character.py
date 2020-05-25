import Global
import pygame

class Character():
    speed = 2.5
    jump_height = 10

    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y

    def render(self):
        pygame.draw.rect(Global.screen, Global.Color.get("Pink"),
                        (self.x, self.y, 50, 50))

    def move(self, dir):
        print(self.x)
        if(dir == "Left"):
            self.x -= self.speed
        if(dir == "Right"):
            self.x += self.speed

    def jump():
        pass
