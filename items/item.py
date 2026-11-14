import pygame as pg

class Item(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, img, picked_up=False):
        super().__init__()
        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.img = pg.image.load(img)
        self.img = pg.transform.scale(self.img, (width, height))
        self.rect = self.img.get_rect(center=(x, y))

        self.speed = 1


        self.picked_up = picked_up

    def update(self, top, bottom):
        border_top = self.y - top
        border_bottom = self.y + bottom

        self.rect.y += self.speed
        if self.rect.top >= border_top:
            self.speed = -self.speed
        elif self.rect.bottom <= border_bottom:
            self.speed = -self.speed