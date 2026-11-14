import pygame as pg

from player import Player
from enemy import Enemy
from items.camera import Camera
from items.battery import Battery

import sqlite3

pg.init()
pg.mixer.init()
width = 1300
height = 700

connection = sqlite3.connect('GameData.db')
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS items (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
number INTEGER DEFAULT NULL)''')

connection.commit()

clock = pg.time.Clock()
FPS = 30

shutter_timer = 0
flash_alpha = 0

timer_duration = 45
end_time = 0
remaining_time = 0
seconds = 15000

timer_active = False
timer_paused = False

player_unfreeze_time = 0

enemy_already_hit = False

camera_allowed = True

background_img = pg.image.load('images/backgrounds/background_hallway.png')
background_img = pg.transform.scale(background_img, (width, height))

window = pg.display.set_mode((width, height))
pg.display.set_caption('Dead Archive')
pg.mouse.set_visible(False)

ENEMY_DATA = {
    1: [
        pg.transform.scale(pg.image.load('images/enemy/enemy_1.png').convert_alpha(), (200, 120)),
        pg.transform.scale(pg.image.load('images/enemy/enemy_reverse_1.png').convert_alpha(), (200, 120))
    ],
    2: [
        pg.transform.scale(pg.image.load('images/enemy/enemy_reverse_2.png').convert_alpha(), (100, 80)),
        pg.transform.scale(pg.image.load('images/enemy/enemy_2.png').convert_alpha(), (100, 80)),
    ],
    3: [
        pg.transform.scale(pg.image.load('images/enemy/enemy_3.png').convert_alpha(), (120, 200))
    ],
    4: [
        pg.transform.scale(pg.image.load('images/enemy/enemy_4.png').convert_alpha(), (200, 200)),
        pg.transform.scale(pg.image.load('images/enemy/enemy_reverse_4.png').convert_alpha(), (200, 200))
    ],
    5: [
        pg.transform.scale(pg.image.load('images/enemy/enemy_5.png').convert_alpha(), (100, 100))
    ]
}

walls_hallway = [
    pg.Rect(0, 0, 300, 105),
    pg.Rect(220, 0, 85, 230),
    pg.Rect(320, 0, 35, 200),
    pg.Rect(0, 0, 40, 280),
    pg.Rect(300, 0, 1000, 60),
    pg.Rect(360, 0, 130, 120),
    pg.Rect(836, 0, 700, 120),
    pg.Rect(1250, 0, 100, 280),
    pg.Rect(0, 569, 525, 280),
    pg.Rect(0, 385, 40, 280),
    pg.Rect(226, 465, 300, 280),
    pg.Rect(468, 410, 165, 30),
    pg.Rect(730, 410, 165, 30),
    pg.Rect(832, 410, 65, 300),
    pg.Rect(500, 643, 350, 100),
    pg.Rect(580, 590, 180, 100),
    pg.Rect(690, 547, 40, 50),
    pg.Rect(832, 467, 225, 300),
    pg.Rect(1000, 569, 300, 300),
    pg.Rect(1245, 385, 60, 300)
]
walls_wards = [
    pg.Rect(0, 0, 1300, 105),
    pg.Rect(0, 0, 150, 300),
    pg.Rect(1205, 0, 300, 800),
    pg.Rect(0, 652, 1300, 100),
    pg.Rect(0, 460, 150, 500),
    pg.Rect(0, 300, 218, 20),
    pg.Rect(410, 105, 80, 130),
    pg.Rect(685, 105, 80, 130),
    pg.Rect(960, 105, 80, 130),
    pg.Rect(410, 460, 80, 200),
    pg.Rect(685, 460, 80, 200),
    pg.Rect(960, 460, 80, 200),
    pg.Rect(348, 518, 40, 10),
    pg.Rect(610, 518, 40, 10),
    pg.Rect(890, 518, 40, 10),
    pg.Rect(507, 573, 38, 10),
    pg.Rect(788, 573, 38, 10),
    pg.Rect(1065, 573, 38, 10),
    pg.Rect(328, 110, 60, 10),
    pg.Rect(500, 110, 200, 10),
    pg.Rect(750, 110, 200, 10),
    pg.Rect(788, 150, 40, 10),
    pg.Rect(495, 150, 40, 10),
    pg.Rect(1150, 330, 40, 10),
    pg.Rect(1075, 130, 40, 10),
    pg.Rect(1150, 170, 40, 10),
    pg.Rect(830, 465, 35, 50),
    pg.Rect(0, 0, 35, height)
]
walls_warehouse = [
    pg.Rect(0, 0, 1300, 70),
    pg.Rect(243, 0, 1200, 120),
    pg.Rect(243, 0, 230, 140),
    pg.Rect(460, 0, 40, 150),
    pg.Rect(648, 0, 60, 160),
    pg.Rect(708, 0, 165, 140),
    pg.Rect(1005, 0, 60, 140),
    pg.Rect(0, 0, 42, 800),
    pg.Rect(0, 0, 75, 205),
    pg.Rect(0, 640, 1300, 205),
    pg.Rect(243, 633, 300, 205),
    pg.Rect(0, 567, 258, 300),
    pg.Rect(455, 567, 390, 300),
    pg.Rect(1153, 0, 300, 285),
    pg.Rect(1153, 450, 300, 285),
    pg.Rect(1260, 390, 10, 100),
    pg.Rect(0, 410, 75, 500),
    pg.Rect(610, 450, 132, 500),
    pg.Rect(538, 530, 50, 500),
    pg.Rect(561, 495, 30, 500),
    pg.Rect(260, 560, 80, 500),
    pg.Rect(925, 550, 75, 500),
    pg.Rect(1080, 549, 75, 500),
    pg.Rect(60, 490, 55, 500),
    pg.Rect(0, 325, 100, 500),
    pg.Rect(160, 450, 100, 10),
    pg.Rect(330, 445, 105, 10),
    pg.Rect(326, 250, 250, 15),
    pg.Rect(785, 265, 260, 25),
    pg.Rect(500, 250, 80, 30),
    pg.Rect(918, 445, 148, 1),
    pg.Rect(1250, 0, 100, height)
]
walls_operating_room = [
    pg.Rect(0, 0, 1300, 85),
    pg.Rect(0, 0, 40, 800),
    pg.Rect(1260, 0, 40, 800),
    pg.Rect(0, 596, 568, 100),
    pg.Rect(710, 596, 568, 100),
    pg.Rect(430, 570, 138, 100),
    pg.Rect(710, 570, 120, 100),
    pg.Rect(0, 0, 80, 450),
    pg.Rect(0, 320, 100, 100),
    pg.Rect(0, 80, 165, 25),
    pg.Rect(218, 80, 20, 20),
    pg.Rect(255, 80, 180, 35),
    pg.Rect(435, 80, 110, 43),
    pg.Rect(466, 80, 20, 60),
    pg.Rect(570, 80, 110, 90),
    pg.Rect(700, 80, 130, 40),
    pg.Rect(840, 80, 27, 20),
    pg.Rect(920, 80, 55, 20),
    pg.Rect(1020, 80, 55, 10),
    pg.Rect(1046, 80, 300, 35),
    pg.Rect(1220, 100, 300, 135),
    pg.Rect(80, 210, 90, 30),
    pg.Rect(0, 367, 135, 1),
    pg.Rect(130, 470, 200, 100),
    pg.Rect(330, 480, 70, 100),
    pg.Rect(1130, 220, 100, 15),
    pg.Rect(1230, 340, 100, 15),
    pg.Rect(1160, 370, 100, 15),
    pg.Rect(1115, 420, 100, 100),
    pg.Rect(1080, 470, 200, 200),
    pg.Rect(1020, 500, 200, 200),
    pg.Rect(840, 495, 140, 200),
    pg.Rect(640, 200, 100, 10),
    pg.Rect(670, 220, 120, 10),
    pg.Rect(690, 290, 120, 10), #
    pg.Rect(590, 280, 70, 110),
    pg.Rect(540, 280, 70, 40),
    pg.Rect(468, 318, 65, 15),
    pg.Rect(688, 330, 55, 25),
    pg.Rect(760, 370, 35, 1),
    pg.Rect(0, 660, width, 100)
]
walls_office = [
    pg.Rect(0, 0, 1300, 170),
    pg.Rect(0, 0, 420, 800),
    pg.Rect(885, 0, 420, 800),
    pg.Rect(0, 512, 595, 500),
    pg.Rect(705, 512, 580, 500),

    pg.Rect(430, 180, 50, 10),
    pg.Rect(760, 180, 150, 10),
    pg.Rect(535, 335, 220, 10),
    pg.Rect(535, 235, 220, 10),
]

documents_hallway = [
    pg.Rect(600, 580, 20, 20),
    pg.Rect(1130, 120, 10, 10)
]
documents_wards = [pg.Rect(805, 570, 10, 10)]
documents_operating_room = [pg.Rect(705, 370, 10, 10)]
documents_warehouse = [pg.Rect(400, 460, 10, 10)]
documents_office = [pg.Rect(700, 340, 20, 20)]


power_battery = 3
count_documents = 0

battery_state = [pg.transform.scale(pg.image.load('images/battery/battery_0.png').convert_alpha(), (70, 40)),
                 pg.transform.scale(pg.image.load('images/battery/battery_1.png').convert_alpha(), (70, 40)),
                 pg.transform.scale(pg.image.load('images/battery/battery_2.png').convert_alpha(), (70, 40)),
                 pg.transform.scale(pg.image.load('images/battery/battery_3.png').convert_alpha(), (70, 40))]

player = Player(100, 155, walls_hallway)
enemy_1 = Enemy(250, 350, 1, 6, ENEMY_DATA)
enemy_2 = Enemy(250, 380, 2, 9, ENEMY_DATA)
enemy_3 = Enemy(398, 410, 3, 0, ENEMY_DATA)
enemy_4 = Enemy(300, 400, 4, 3, ENEMY_DATA)
enemy_5 = Enemy(205, 100, 5, 0, ENEMY_DATA)

camera = Camera(735, 590)

battery1 = Battery(235, 475)
battery2 = Battery(100, 480)
battery3 = Battery(1130, 200)

battery3.rect.width = 50
battery3.rect.height = 50

font = pg.font.SysFont('Arial Bold', 250)
text_game_over = font.render('Game Over :)', True, (255, 255, 255))
text_game_win = font.render('Congratulations!', True, (255, 255, 255))

batteries = [battery1, battery2, battery3]
enemies = [enemy_1, enemy_2, enemy_3, enemy_4, enemy_5]

sound_closed_door = pg.mixer.Sound('sounds/closed_door.ogg')
sound_turn_off = pg.mixer.Sound('sounds/turn_off.ogg')
sound_flash = pg.mixer.Sound('sounds/camera_flash.ogg')
sound_take_item = pg.mixer.Sound('sounds/take_item.ogg')

sound_legs = pg.mixer.Sound('sounds/sound_legs.ogg')
sound_ghost = pg.mixer.Sound('sounds/sound_ghost.ogg')
sound_voice = pg.mixer.Sound('sounds/sound_voice.ogg')
sound_wheels = pg.mixer.Sound('sounds/sound_wheels.ogg')
sound_cry = pg.mixer.Sound('sounds/sound_cry.ogg')
sound_run = pg.mixer.Sound('sounds/sound_run.ogg')

game_over_sound = pg.mixer.Sound('sounds/game_over.ogg')
laugh_sound = pg.mixer.Sound('sounds/laugh_sound.ogg')
game_win_sound = pg.mixer.Sound('sounds/game_win.ogg')

sound_find_item = pg.mixer.Sound('sounds/find_item.ogg')
sound_search = pg.mixer.Sound('sounds/search.ogg')

sound_heart = pg.mixer.Sound('sounds/sound_heart.ogg')

channel_search = pg.mixer.Channel(5)

sound_find_item_started = False
sound_search_started = False

sounds_enemies = [sound_legs, sound_ghost, sound_voice, sound_wheels, sound_run]

pg.mixer.music.load('music/main_music.ogg')
past_music = pg.mixer.Sound('music/past_music.ogg')
music_channel = pg.mixer.Channel(0)

past_music_paused = False

pg.mixer.music.play(-1)
pg.mixer.music.set_volume(0.5)
laugh_sound.set_volume(0.5)

past_music.set_volume(0.2)


legs_playing = False
ghost_playing = False
voice_playing = False
wheels_playing = False
cry_playing = False

game_over_running = False

RED = (255, 0, 0)
BLACK = (0, 0, 0)
PURPLE = (70,57,75)
PURPLE_ALPHA = (84, 57, 100, 100)

light_radius = 60
light_mask = pg.Surface((width, height), pg.SRCALPHA).convert_alpha()
flash_mask = pg.Surface((width, height), pg.SRCALPHA).convert_alpha()

operating_past_timer = 0
operating_timer_active = False

fade_surface = pg.Surface((width, height))

rooms = {
    'Hallway': {
        'background': pg.transform.scale(pg.image.load('images/backgrounds/background_hallway.png').convert(), (width, height)),
        'left': 'Warehouse',
        'right': 'Wards',
        'up': 'Operating_room',
        'walls': walls_hallway
    },
    'Wards': {
        'background': pg.transform.scale(pg.image.load('images/backgrounds/background_wards.png').convert(), (width, height)),
        'left': 'Hallway',
        'walls': walls_wards
    },
    'Warehouse': {
        'background': pg.transform.scale(pg.image.load('images/backgrounds/background_warehouse.png').convert(), (width, height)),
        'right': 'Hallway',
        'up': 'Office',
        'walls': walls_warehouse
    },
    'Operating_room': {
        'background': pg.transform.scale(pg.image.load('images/backgrounds/background_operating_room.png').convert(), (width, height)),
        'down': 'Hallway',
        'walls': walls_operating_room
    },
     'Office': {
            'background': pg.transform.scale(pg.image.load('images/backgrounds/background_office.png').convert(), (width, height)),
             'down': 'Warehouse',
             'walls': walls_office
        }
}
rooms_past = {
    'Hallway': {
        'background': pg.transform.scale(pg.image.load('images/backgrounds/background_false_hallway.png').convert(), (width, height)),
        'left': 'Warehouse',
        'right': 'Wards',
        'up': 'Operating_room',
        'walls': walls_hallway
    },
    'Wards': {
        'background': pg.transform.scale(pg.image.load('images/backgrounds/background_false_wards.png').convert(), (width, height)),
        'left': 'Hallway',
        'walls': walls_wards
    },
    'Warehouse': {
        'background': pg.transform.scale(pg.image.load('images/backgrounds/background_false_warehouse.png').convert(), (width, height)),
        'right': 'Hallway',
        'up': 'Office',
        'walls': walls_warehouse
    },
    'Operating_room': {
        'background': pg.transform.scale(pg.image.load('images/backgrounds/background_false_operating_room.png').convert(), (width, height)),
        'down': 'Hallway',
        'walls': walls_operating_room
    },
    'Office': {
        'background': pg.transform.scale(pg.image.load('images/backgrounds/background_false_office.png').convert(), (width, height)),
        'down': 'Warehouse',
        'walls': walls_office
    }
}

active_room = 'Hallway'
doors = [pg.Rect(565, 0, 50, 85)]
closed_doors = [pg.Rect(100, 0, 50, 120)]

def change_room(room_name, spawn_side):
    global background_img, active_room, player, doors, closed_doors

    active_room = room_name
    if camera.camera_on and power_battery != 0:
        room_data = rooms_past[room_name]
    else:
        room_data = rooms[room_name]

    background_img = room_data['background']
    player.walls = room_data['walls']

    if spawn_side == 'left' and room_name == 'Wards':
        player.rect.left = 50
        player.rect.top = 340
    elif  spawn_side == 'left' and room_name == 'Hallway':
        player.rect.left = 50
    elif spawn_side == 'right' and room_name == 'Warehouse':
        player.rect.right = width - 50
        player.rect.bottom = 390
    elif spawn_side == 'right' and room_name == 'Hallway':
        player.rect.right = width - 50
        player.rect.bottom = 380
    elif spawn_side == 'down':
        player.rect.top = height - 150
        player.rect.left = 610
    elif spawn_side == 'up' and room_name == 'Warehouse':
        player.rect.top = 100
        player.rect.left = 100
    elif spawn_side == 'up':
        player.rect.top = 100
        player.rect.left = 570

    if active_room == 'Hallway':
        doors = [pg.Rect(565, 0, 50, 85)]
        closed_doors = [pg.Rect(100, 0, 50, 120)]
    elif active_room == 'Warehouse':
        doors = [pg.Rect(1230, 350, 100, 40)]
        closed_doors = [pg.Rect(120, 0, 50, 80)]
    elif active_room == 'Operating_room':
        doors = [pg.Rect(565, 640, 150, 85)]
        closed_doors = [pg.Rect(0, 0, 0, 0)]
    elif active_room == 'Wards':
        doors = [pg.Rect(0, 320, 50, 120)]
        closed_doors = [pg.Rect(0, 0, 0, 0)]
    elif active_room == 'Office':
        doors = [pg.Rect(565, 640, 150, 85)]
        closed_doors = [pg.Rect(0, 0, 0, 0)]
    else:
        doors = [pg.Rect(0, 0, 0, 0)]
        closed_doors = [pg.Rect(0, 0, 0, 0)]

def draw():
    global flash_alpha, power_battery, count_documents

    window.fill((0, 0, 0))
    window.blit(background_img, (0, 0))

    font_fine = pg.font.SysFont('Arial', 40)
    text_find = font_fine.render((f'Собрано: {count_documents} из 6'), True, (255, 255, 255))

    if camera.picked_up and active_room == 'Operating_room':
        window.blit(enemy_5.img, enemy_5.rect)

    window.blit(player.img, player.rect)

    if not camera.camera_on and camera.picked_up:
        if active_room == 'Hallway':
            window.blit(enemy_1.img, enemy_1.rect)
        elif active_room == 'Wards':
            window.blit(enemy_2.img, enemy_2.rect)
        elif active_room == 'Warehouse':
            window.blit(enemy_3.img, enemy_3.rect)
        elif active_room == 'Operating_room':
            window.blit(enemy_4.img, enemy_4.rect)

    if not camera.picked_up and active_room == 'Hallway':
        window.blit(camera.img, camera.rect)
    elif camera.picked_up:
        if not battery1.picked_up and active_room == 'Operating_room' and not camera.camera_on:
            window.blit(battery1.img, battery1.rect)

        if not battery2.picked_up and active_room == 'Warehouse' and not camera.camera_on:
            window.blit(battery2.img, battery2.rect)

        if pg.time.get_ticks() >= shutter_timer:
            if not camera.camera_on:
                update_flashlight(light_mask, [player.rect.x + 25, player.rect.y + 50], 80)
                window.blit(light_mask, (0, 0))

        window.blit(battery_state[power_battery], (1220, 10))
        window.blit(text_find, (20, 10))

    if flash_alpha > 0:
        flash_mask.fill(BLACK)
        flash_mask.set_alpha(flash_alpha)
        window.blit(flash_mask, (0, 0))
        flash_alpha -= 15

    if flash_alpha <= 0:
        flash_alpha = 0

def fade_out(surface, color):
    surface.fill(color)

    for alpha in range(0, 256, 5):
        surface.set_alpha(alpha)
        draw()
        window.blit(surface, (0, 0))

        pg.display.flip()
        pg.time.delay(10)

def fade_in(surface, color):
    surface.fill(color)
    for alpha in range(255, -1, -5):
        surface.set_alpha(alpha)
        draw()
        window.blit(surface, (0, 0))

        pg.display.flip()
        pg.time.delay(20)

def pick_up_item(name, num=None):
    global player_unfreeze_time, sound_find_item_started, sound_search_started, channel_search

    cursor.execute('''INSERT OR IGNORE INTO items (name, number) VALUES (?, ?)''', (name, num))
    connection.commit()


    if name == 'camera':
        return
    else:
        player_unfreeze_time = pg.time.get_ticks() + 2000

        channel_search.play(sound_search)
        channel_search.queue(sound_find_item)
        sound_search_started = True
        sound_find_item_started = True

    print('o')

def update_flashlight(mask, pos, radius):
    mask.fill((0, 0, 0, 220))
    pg.draw.circle(mask, (0, 0, 0, 120), pos, radius)

def flash():
    global shutter_timer, camera, background_img, doors, closed_doors, flash_alpha

    sound_flash.play()
    camera.camera_on = not camera.camera_on

    if camera.camera_on:
        room_data = rooms_past[active_room]
        background_img = room_data['background']
        player.walls = room_data['walls']
        if not timer_active:
            start_timer(timer_duration)
        else:
            resume_timer()
    else:
        room_data = rooms[active_room]
        background_img = room_data['background']
        player.walls = room_data['walls']
        pause_timer()

    if active_room == 'Hallway':
        doors = [pg.Rect(565, 0, 50, 85)]
        closed_doors = [pg.Rect(100, 0, 50, 120)]
    elif active_room == 'Warehouse':
        doors = [pg.Rect(1230, 350, 100, 40)]
        closed_doors = [pg.Rect(120, 0, 50, 80)]
    elif active_room == 'Operating_room':
        doors = [pg.Rect(565, 640, 150, 85)]
        closed_doors = [pg.Rect(0, 0, 0, 0)]
    elif active_room == 'Wards':
        doors = [pg.Rect(0, 320, 50, 120)]
        closed_doors = [pg.Rect(0, 0, 0, 0)]

    flash_alpha = 255
    shutter_timer = pg.time.get_ticks()

def start_timer(seconds):
    global end_time, timer_active, timer_paused
    current_time = pg.time.get_ticks()

    end_time = current_time + (seconds * 1000)

    timer_active = True
    timer_paused = False

def pause_timer():
    global end_time, remaining_time, timer_active, timer_paused

    if timer_active and not timer_paused:
        current_time = pg.time.get_ticks()
        timer_paused = True

        remaining_time = end_time - current_time
        print("Осталось:", remaining_time / 1000)

def resume_timer():
    global end_time, timer_paused

    if timer_active and timer_paused:
        current_time = pg.time.get_ticks()
        end_time = current_time + remaining_time

        timer_paused = False

def game_over():
    global game_over_running, state, sounds_enemies
    for sound in sounds_enemies:
        sound.stop()

    laugh_sound.play()
    game_over_sound.play()

    window.fill((0, 0, 0))
    window.blit(text_game_over, (120, 230))

    pg.display.flip()
    pg.time.delay(5000)
    state = False

def game_win():
    global state
    for sound in sounds_enemies:
        sound.stop()

    game_win_sound.play()
    pg.mixer.music.pause()
    window.fill((0, 0, 0))
    window.blit(text_game_win, (120, 230))

    pg.display.flip()
    pg.time.delay(5000)
    state = False

state = True
while state:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            state = False
        elif event.type == pg.KEYDOWN:

            if event.key == pg.K_e:
                if player.rect.left <= 0 or (player.rect.colliderect(doors[0]) and active_room == 'Wards'):
                    next_room = rooms[active_room].get('left')
                    if next_room:
                        fade_out(fade_surface, BLACK)
                        change_room(next_room, 'right')
                        fade_in(fade_surface, BLACK)

                elif player.rect.right >= width or (player.rect.colliderect(doors[0]) and active_room == 'Warehouse'):
                    next_room = rooms[active_room].get('right')
                    if next_room:
                        fade_out(fade_surface, BLACK)
                        change_room(next_room, 'left')
                        fade_in(fade_surface, BLACK)

                elif player.rect.colliderect(camera.rect) and not camera.picked_up and active_room == 'Hallway':
                    sound_turn_off.play()
                    camera.picked_up = True
                    pick_up_item(camera.name)
                    print('берет')

                elif player.rect.colliderect(battery1.rect) and not battery1.picked_up and active_room == 'Operating_room' and not camera.camera_on:
                    if power_battery < 3:
                        sound_take_item.play()
                        battery1.picked_up = True
                        pick_up_item(battery1.name)

                        camera_allowed = True
                        timer_active = True

                        if timer_paused:
                            remaining_time += seconds
                        else:
                            end_time += seconds
                        print('берет батарейку 1')

                elif player.rect.colliderect(battery2.rect) and not battery2.picked_up and active_room == 'Warehouse' and not camera.camera_on:
                    if power_battery < 3:

                        sound_take_item.play()
                        battery2.picked_up = True
                        pick_up_item(battery2.name)

                        camera_allowed = True
                        timer_active = True

                        if timer_paused:
                            remaining_time += seconds
                        else:
                            end_time += seconds
                        print('берет батарейку 2')

                elif player.rect.colliderect(battery3.rect) and not battery3.picked_up and active_room == 'Wards' and not camera.camera_on and camera.picked_up:
                    if power_battery < 3:
                        sound_take_item.play()
                        battery3.picked_up = True
                        pick_up_item(battery3.name)

                        camera_allowed = True
                        timer_active = True

                        if timer_paused:
                            remaining_time += 10000
                        else:
                            end_time += 10000
                        print('берет батарейку 3')

                elif player.rect.colliderect(doors[0]):
                    if active_room == 'Hallway':
                        next_room = rooms[active_room].get('up')
                    else:
                        next_room = rooms[active_room].get('down')

                    if next_room:
                        fade_out(fade_surface, BLACK)
                        if active_room == 'Hallway':
                            change_room(next_room, 'down')
                        else:
                            change_room(next_room, 'up')
                        fade_in(fade_surface, BLACK)
                    if active_room == 'Office':
                        if camera.camera_on:
                            next_room = rooms_past[active_room].get('down')
                        else:
                            next_room = rooms[active_room].get('down')

                        if next_room:
                            fade_out(fade_surface, BLACK)
                            change_room(next_room, 'up')
                            fade_in(fade_surface, BLACK)

                elif player.rect.colliderect(closed_doors[0]):
                    if active_room == 'Warehouse' and camera.camera_on:
                        next_room = rooms_past[active_room].get('up')
                        if next_room:
                            fade_out(fade_surface, BLACK)
                            change_room(next_room, 'down')
                            fade_in(fade_surface, BLACK)
                    elif active_room == 'Hallway' and count_documents == 6:
                        game_win()
                    else:
                        sound_closed_door.play()
                        print('не')

                elif camera.picked_up and not camera.camera_on:
                    if active_room == 'Hallway':
                        for i in range(len(documents_hallway)):
                            if player.rect.colliderect(documents_hallway[i]):
                                pick_up_item(f'document_hallway_{i}')
                                del documents_hallway[i]
                                count_documents += 1

                                print('УРА')
                                break

                    elif active_room == 'Operating_room':
                        for i in range(len(documents_operating_room)):
                            if player.rect.colliderect(documents_operating_room[i]):
                                pick_up_item(f'documents_operating_room_{i}')
                                del documents_operating_room[i]
                                count_documents += 1
                                print('УРА')
                                break

                    elif active_room == 'Office':
                        for i in range(len(documents_office)):
                            if player.rect.colliderect(documents_office[i]):
                                count_documents += 1
                                pick_up_item(f'documents_office_{i}')
                                del documents_office[i]
                                print('УРА')
                                break

                elif camera.picked_up and camera.camera_on:
                    if active_room == 'Wards':
                        for i in range(len(documents_wards)):
                            if player.rect.colliderect(documents_wards[i]):
                                pick_up_item(f'documents_wards_{i}')
                                del documents_wards[i]
                                count_documents += 1
                                print('УРА')
                                break

                    elif active_room == 'Warehouse':
                        for i in range(len(documents_warehouse)):
                            if player.rect.colliderect(documents_warehouse[i]):
                                pick_up_item(f'documents_warehouse_{i}')
                                del documents_warehouse[i]
                                count_documents += 1
                                print('УРА')
                                break

            if event.key == pg.K_SPACE and camera.picked_up:
                if camera_allowed:
                    flash()

    if player.rect.left < 0:
        player.rect.left = 0
    if player.rect.right > width:
        player.rect.right = width
    if player.rect.top < 0:
        player.rect.top = 0
    if player.rect.bottom > height:
        player.rect.bottom = height

    collision_with_enemy = (
            (player.rect.colliderect(enemy_1.rect) and active_room == 'Hallway') or
            (player.rect.colliderect(enemy_2.rect) and active_room == 'Wards') or
            (player.rect.colliderect(enemy_3.rect) and active_room == 'Warehouse') or
            (player.rect.colliderect(enemy_4.rect) and active_room == 'Operating_room') or
            (player.rect.colliderect(enemy_5.rect) and active_room == 'Operating_room')
    )

    if not camera.camera_on and camera.picked_up:
        if collision_with_enemy:
            game_over()

    elif camera.picked_up and camera.camera_on:
        if collision_with_enemy:
            if not enemy_already_hit:
                sound_heart.play(-1)
                enemy_already_hit = True
        else:
            sound_heart.stop()
            enemy_already_hit = False


    if timer_active:
        if timer_paused:
            time_left = remaining_time
        else:
            time_left = end_time - pg.time.get_ticks()

        seconds_left = max(0.0, time_left / 1000)


        if seconds_left > 20:
            power_battery = 3
        elif seconds_left > 10:
            power_battery = 2
        elif seconds_left > 0:
            power_battery = 1
        else:
            flash()
            power_battery = 0
            timer_active = False
            camera_allowed = False


    if not camera.camera_on and active_room == 'Hallway' and camera.picked_up:
        if not legs_playing:
            sound_legs.play(-1)
            legs_playing = True
    else:
        if legs_playing:
            sound_legs.stop()
            legs_playing = False

    if not camera.camera_on and active_room == 'Operating_room' and camera.picked_up:
        if not ghost_playing:
            sound_ghost.play(-1)
            ghost_playing = True
    else:
        if ghost_playing:
            sound_ghost.stop()
            ghost_playing = False

    if active_room == 'Warehouse' and camera.picked_up:
        if not voice_playing:
            sound_voice.play(-1)
            voice_playing = True
    else:
        if voice_playing:
            sound_voice.stop()
            voice_playing = False


    if active_room == 'Office' and camera.picked_up:
        if not cry_playing:
            sound_cry.play(-1)
            cry_playing = True
    else:
        if cry_playing:
            sound_cry.stop()
            cry_playing = False


    if not camera.camera_on and active_room == 'Wards' and camera.picked_up:
        if not wheels_playing:
            sound_wheels.play(-1)
            wheels_playing = True
    else:
        if wheels_playing:
            sound_wheels.stop()
            wheels_playing = False


    if not camera.picked_up or camera.camera_on:
        pg.mixer.music.pause()
    else:
        pg.mixer.music.unpause()


    if camera.picked_up and camera.camera_on and not music_channel.get_busy():
        music_channel.play(past_music, -1)
        past_music_paused = False


    if camera.camera_on and active_room != 'Warehouse' and active_room != 'Office':
        if past_music_paused:
            music_channel.unpause()
            past_music_paused = False
    else:
        if not past_music_paused:
            music_channel.pause()
            past_music_paused = True

    if player.moving and active_room == 'Operating_room':
        if enemy_4.speed < 0:
            enemy_4.speed = -14
        else:
            enemy_4.speed = 14
    else:
        if enemy_4.speed < 0:
            enemy_4.speed = -3
        else:
            enemy_4.speed = 3

    if active_room == 'Operating_room' and camera.camera_on:

        if not operating_timer_active:
            sound_run.play()
            music_channel.pause()

            operating_past_timer = pg.time.get_ticks() + 5000
            operating_timer_active = True

        elif operating_timer_active:
            if pg.time.get_ticks() >= operating_past_timer:
                operating_timer_active = False

                if not enemy_already_hit:
                    sound_heart.play(-1)
                    enemy_already_hit = True
                else:
                    sound_heart.stop()
                    enemy_already_hit = False

                game_over()
    else:
        if operating_timer_active:
            operating_timer_active = False


    camera.update(15, 15)

    for battery in batteries:
        battery.update(35, 25)

    player.update(player_unfreeze_time)
    enemy_1.update('x', 100, 400)
    enemy_2.update('x', 200, 900)
    enemy_3.update('y', 50, 290)
    enemy_4.update('x', 200, 900)
    draw()

    # for walls in walls_office:
    clock.tick(FPS)
    pg.display.update()

