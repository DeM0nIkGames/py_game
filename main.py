import pygame
import os
from random import randint


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


def first_map():
    Box(200, 200)
    Box(550, 550)
    Box(200, 550)
    Box(550, 200)


def main_fire(hero, direction):
    bullet = Bullet(hero, direction, False)
    bullet.add(good_bullets)


def enemy_fire(x, y, direction):
    bullet = EnemyBullets(x, y, direction)
    bullet.add(bad_bullets)


all_sprites = pygame.sprite.Group()
pygame.init()
screen_size = (800, 800)
screen = pygame.display.set_mode(screen_size)
FPS = 50
clock = pygame.time.Clock()
left = load_image("left_goat.png")
right = load_image("right_goat.png")
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
main_character = pygame.sprite.Group()
bad_bullets = pygame.sprite.Group()
good_bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
boxes = pygame.sprite.Group()
main = pygame.sprite.Group()
e_l = AnimatedSprite(load_image("enemy_left.png"), 3, 1, 800, 800)
e_r = AnimatedSprite(load_image("enemy_right.png"), 3, 1, 800, 800)
goat_left = AnimatedSprite(load_image("goat_ani_1.png"), 6, 1, 800, 800)
goat_right = AnimatedSprite(load_image("goat_ani.png"), 6, 1, 800, 800)
# left_enemy = AnimatedSprite(load_image("enemy_left.png"), 3, 2, 200, 200)
# right_enemy = AnimatedSprite(load_image("enemy_right.png"), 3, 2, 300, 300)
floor = load_image("floor.png")
vertical = load_image("horizontal.png")
horizontal = load_image("vertical.png")
enemy_left = load_image("enemy_left.png")
enemy_right = load_image("enemy_right.png")
rockets = pygame.sprite.Group()
bosses = pygame.sprite.Group()


class FirstBoss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = e_r.image
        self.rect = self.image.get_rect().move(x, y)
        self.hp = 50
        self.dir = "right"
        self.x = self.rect.x
        self.y = self.rect.y
        self.counter = 10
        self.add(bosses)

    def move(self):
        move = randint(1, 5)
        if move == 1:
            self.image = e_l.image
            self.rect.x -= 10
            self.x = self.rect.x
            self.y = self.rect.y
            self.dir = "left"
        elif move == 2:
            self.image = e_r.image
            self.rect.x += 10
            self.x = self.rect.x
            self.y = self.rect.y
            self.dir = "right"
        elif move == 3:
            self.rect.y += 10
            self.x = self.rect.x
            self.y = self.rect.y
        else:
            self.rect.y -= 10
            self.x = self.rect.x
            self.y = self.rect.y
        if self.rect.x + 4 > 700:
            self.rect.x -= 10
            self.x = self.rect.x
            self.y = self.rect.y
        elif self.rect.x - 4 < 50:
            self.rect.x += 10
            self.x = self.rect.x
            self.y = self.rect.y
        elif self.rect.y + 4 > 700:
            self.rect.y -= 10
            self.x = self.rect.x
            self.y = self.rect.y
        elif self.rect.y - 4 < 50:
            self.rect.y += 10
            self.x = self.rect.x
            self.y = self.rect.y

    def shoot(self, dir):
        if dir == "left":
            self.dir = "left"
            self.image = e_l.image
        else:
            self.dir = "right"
            self.image = e_r.image
        enemy_fire(self.x, self.y, self.dir)

    def rockets(self):
        if self.dir == "left":
            Rockets(self.x, self.y, "left")
        else:
            Rockets(self.x, self.y, "right")

    def update(self):
        if pygame.sprite.spritecollide(self, good_bullets, True):
            self.hp -= 1
        if self.hp <= 0:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, hero, direction, bad):
        super().__init__(all_sprites)
        self.image = load_image("bullet.png")
        self.rect = self.image.get_rect().move(hero.rect.x + 10, hero.rect.y + 10)
        if direction == 'left':
            self.vx = -40
        else:
            self.vx = 40
        if bad:
            self.add(bad_bullets)
        else:
            self.add(good_bullets)

    def update(self):
        self.rect.x += self.vx
        if pygame.sprite.spritecollide(self, horizontal_borders, True) or pygame.sprite.spritecollide(self, vertical_borders, True) or pygame.sprite.spritecollide(self, boxes, False):
            self.remove(all_sprites)


class EnemyBullets(pygame.sprite.Sprite):
    def __init__(self, x, y, direction="untitled", vx=0, vy=0):
        super().__init__(all_sprites)
        self.image = load_image("bullet.png")
        self.rect = self.image.get_rect().move(x + 10, y + 10)
        if direction == "left":
            self.vx = -10
        elif direction == "right":
            self.vx = 10
        else:
            self.vx = vx
        self.vy = vy
        self.add(bad_bullets)

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if pygame.sprite.spritecollide(self, horizontal_borders, True) or pygame.sprite.spritecollide(self, vertical_borders, True) or pygame.sprite.spritecollide(self, boxes, False):
            self.remove(all_sprites)


class Rockets(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__(all_sprites)
        if direction == 'left':
            self.vx = -5
            self.image = load_image("rocket_left.png")
        else:
            self.vx = 5
            self.image = load_image("rocket.png")
        self.rect = self.image.get_rect().move(x + 10, y + 10)
        self.add(rockets)

    def update(self):
        self.rect.x += self.vx
        if pygame.sprite.spritecollide(self, horizontal_borders, True) or pygame.sprite.spritecollide(self, vertical_borders, True) or pygame.sprite.spritecollide(self, boxes, False):
            EnemyBullets(self.rect.x, self.rect.y, vx=-10, vy=0)
            EnemyBullets(self.rect.x, self.rect.y, vx=10, vy=0)
            EnemyBullets(self.rect.x, self.rect.y, vx=0, vy=10)
            EnemyBullets(self.rect.x, self.rect.y, vx=0, vy=-10)
            EnemyBullets(self.rect.x, self.rect.y, vx=10, vy=-10)
            EnemyBullets(self.rect.x, self.rect.y, vx=-10, vy=-10)
            EnemyBullets(self.rect.x, self.rect.y, vx=-10, vy=10)
            EnemyBullets(self.rect.x, self.rect.y, vx=10, vy=10)
            self.remove(all_sprites)


class Box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(boxes)
        self.image = load_image("box.png")
        self.rect = pygame.Rect(x, y, 100, 100)


class Border(pygame.sprite.Sprite):
    def __init__(self, vert, x, y):
        super().__init__(all_sprites)
        if vert:
            self.add(vertical_borders)
            self.image = vertical
            self.rect = pygame.Rect(x, y, 50, 800)
        else:
            self.add(horizontal_borders)
            self.image = horizontal
            self.rect = pygame.Rect(x, y, 800, 50)


class MainCharacter(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = goat_right.image
        self.rect = self.image.get_rect().move(x - 50, y - 50)
        self.vx, self.vy = 0, 0
        self.add(main)
        self.hp = 5
        self.dir = right

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.vx = 0
        self.vy = 0
        if pygame.sprite.spritecollide(self, bad_bullets, True):
            self.hp -= 1
        if pygame.sprite.spritecollide(self, rockets, True):
            self.hp -= 2
        self.rect = self.rect.move(self.vx, self.vy)

    def move(self, movement):
        if movement == "up":
            self.vy -= 10
        elif movement == "down":
            self.vy += 10
        elif movement == "left":
            self.dir = left
            self.vx -= 10
        elif movement == "right":
            self.dir = right
            self.vx += 10
        if self.rect.x + 10 > 700:
            self.rect.x -= 20
        elif self.rect.x - 10 < 50:
            self.rect.x += 20
        elif self.rect.y + 10 > 700:
            self.rect.y -= 20
        elif self.rect.y - 10 < 50:
            self.rect.y += 20


def main_death():
    going = True
    while going:
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 50)
        text = font.render("Игра окончена", True, (100, 100, 255))
        screen.blit(text, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos


p, e = 0, 0


def game_cycle():
    running = True
    pers = MainCharacter(150, 150)
    en = FirstBoss(650, 650)
    global p, e
    p = pers.hp
    e = en.hp
    first_map()
    while running:
        if pers.hp <= 0 or en.hp <= 0:
            p = pers.hp
            e = en.hp
            pers.kill()
            en.kill()
            running = False
        Border(1, 0, 0)
        Border(0, 0, 0)
        Border(0, 0, 750)
        Border(1, 750, 0)
        screen.blit(floor, (0, 0))
        all_sprites.draw(screen)
        vertical_borders.draw(screen)
        horizontal_borders.draw(screen)
        if randint(1, 5) == 1:
            en.move()
        if randint(1, 100) == 1:
            en.rockets()
            if -10 <= en.y - pers.rect.y <= 10:
                if en.x < pers.rect.x:
                    en.shoot("right")
                elif en.x > pers.rect.x:
                    en.shoot("left")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pers.dir == "left":
                    main_fire(pers, "left")
                else:
                    main_fire(pers, "right")
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            pers.move("up")
        elif keys[pygame.K_s]:
            pers.move("down")
        elif keys[pygame.K_a]:
            pers.move("left")
            pers.dir = "left"
            pers.image = goat_left.image
        elif keys[pygame.K_d]:
            pers.move("right")
            pers.dir = "right"
            pers.image = goat_right.image
        pers.update()
        all_sprites.update()
        font = pygame.font.Font(None, 30)
        text = font.render(f"Здоровья осталось у игрока: {pers.hp}", True, (100, 255, 100))
        screen.blit(text, (0, 0))
        font = pygame.font.Font(None, 30)
        text = font.render(f"Здоровья осталось у противника: {en.hp}", True, (100, 255, 100))
        screen.blit(text, (350, 0))
        pygame.display.flip()


game_cycle()
if p != 0:
    while input("Вы победили! Желаете продолжить? ") == "Да":
        game_cycle()
else:    print("К сожалению, Вы проиграли!")
pygame.quit()
