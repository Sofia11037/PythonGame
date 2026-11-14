import pygame as pg

class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y, enemy_type, speed, enemy_data):
        super().__init__()
        self.x = x
        self.y = y
        self.enemy_type = enemy_type

        self.frames = []

        self.frames = enemy_data[enemy_type]
        self.speed = speed

        self.img = self.frames[0]
        self.rect = self.img.get_rect(center=(x, y))



    def update(self, axis, side_1, side_2):
        if axis == 'y':
            border_1 = self.y - side_1
            border_2 = self.y + side_2

            self.rect.y += self.speed
            if self.rect.top <= border_1:
                self.speed = -self.speed
                self.rect.top = border_1 + 1
                self.img = self.frames[0]
            elif self.rect.bottom >= border_2:
                self.speed = -self.speed
                self.rect.bottom = border_2 - 1
                if len(self.frames) > 1:
                    self.img = self.frames[1]

        elif axis == 'x':
            border_1 = self.x - side_1
            border_2 = self.x + side_2

            self.rect.x += self.speed
            if self.rect.left <= border_1:
                self.speed = -self.speed
                self.rect.left = border_1 + 1
                self.img = self.frames[0]

            elif self.rect.right >= border_2:
                self.speed = -self.speed
                self.rect.right = border_2 - 1
                if len(self.frames) > 1:
                    self.img = self.frames[1]

        # self.rect.