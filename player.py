import pygame as pg

class Player(pg.sprite.Sprite):
    def __init__(self, x, y, walls):
        super().__init__()

        self.stand_frames = [
            pg.transform.scale(pg.image.load('images/player/stand.png'), (50, 100)),
        ]

        self.left_frames = [
            pg.transform.scale(pg.image.load('images/player/player_walk_left_one.png'), (50, 100)),
            pg.transform.scale(pg.image.load('images/player/player_walk_left_two.png'), (50, 100))
        ]
        self.right_frames = [
            pg.transform.scale(pg.image.load('images/player/player_walk_right_one.png'), (50, 100)),
            pg.transform.scale(pg.image.load('images/player/player_walk_right_two.png'), (50, 100))
        ]
        self.up_frames = [
            pg.transform.scale(pg.image.load('images/player/player_top_one.png'), (50, 100)),
            pg.transform.scale(pg.image.load('images/player/player_top_two.png'), (50, 100))
        ]
        self.down_frames = [
            pg.transform.scale(pg.image.load('images/player/player_down_one.png'), (50, 100)),
            pg.transform.scale(pg.image.load('images/player/player_down_two.png'), (50, 100))
        ]

        self.direction = ''
        self.current_frame = 0

        self.walls = walls

        self.x = x
        self.y = y

        self.img = pg.image.load('images/player/player_right.png')
        self.img = pg.transform.scale(self.img, (50, 100))
        self.rect = self.img.get_rect(center=(x, y))

        self.animation_counter = 0
        self.animation_speed = 8
        self.speed = 8

        self.moving = False

        self.steps = pg.mixer.Sound('sounds/steps.ogg')
        self.sound_playing = False



    def update(self, player_unfreeze_time):

        if pg.time.get_ticks() < player_unfreeze_time:
            self.moving = False
            # self.steps.stop()
            return

        def animate(frame):
            if self.animation_counter >= self.animation_speed:
                self.current_frame = (self.current_frame + 1) % len(frame)
                self.img = frame[self.current_frame]
                self.animation_counter = 0

        self.animation_counter += 1
        key = pg.key.get_pressed()
        self.moving = False


        if key[pg.K_w] or key[pg.K_UP]:
            self.rect.y -= self.speed
            self.direction = 'up'
            self.moving = True
            for wall in self.walls:
                if self.rect.colliderect(wall):
                    self.rect.top = wall.bottom

        if key[pg.K_s] or key[pg.K_DOWN]:
            self.rect.y += self.speed
            self.direction = 'down'
            self.moving = True
            for wall in self.walls:
                if self.rect.colliderect(wall):
                    self.rect.bottom = wall.top

        if key[pg.K_a] or key[pg.K_LEFT]:
            self.rect.x -= self.speed
            self.direction = 'left'
            self.moving = True
            for wall in self.walls:
                if self.rect.colliderect(wall):
                    self.rect.left = wall.right

        if key[pg.K_d] or key[pg.K_RIGHT]:
            self.rect.x += self.speed
            self.direction = 'right'
            self.moving = True
            for wall in self.walls:
                if self.rect.colliderect(wall):
                    self.rect.right = wall.left

        if self.moving:
            if not self.sound_playing:
                self.steps.play(-1)
                self.sound_playing = True

            if self.direction == 'up':
                animate(self.up_frames)
            elif self.direction == 'down':
                animate(self.down_frames)
            elif self.direction == 'left':
                animate(self.left_frames)
            elif self.direction == 'right':
                animate(self.right_frames)
        else:
            if self.sound_playing:
                self.steps.stop()
                self.sound_playing = False
            self.img = self.stand_frames[0]
