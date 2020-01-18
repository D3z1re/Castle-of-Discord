import pygame
from pygame.locals import *
from math import fabs
import sys

pygame.init()
WIDTH, HEIGHT = 1280, 720
TILE_WIDTH = 32
FPS = 60
LEVELS = ['level_1.txt', 'level_2.txt', 'level_3.txt', 'level_4.txt']
FILE = 'level_1.txt'
win = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF)
win.set_alpha(None)
clock = pygame.time.Clock()
pygame.display.set_caption('Castle of Discord')
pygame.mouse.set_visible(False)

# Загрузка заднего фона
bg = pygame.image.load('data/textures/bg.png')

# Загрузка изображений
LEFT_MOVE = [pygame.image.load('data/models/player/left_1.png'), pygame.image.load('data/models/player/left_2.png'),
             pygame.image.load('data/models/player/left_3.png'), pygame.image.load('data/models/player/left_4.png')]
RIGHT_MOVE = [pygame.image.load('data/models/player/right_1.png'), pygame.image.load('data/models/player/right_2.png'),
              pygame.image.load('data/models/player/right_3.png'), pygame.image.load('data/models/player/right_4.png')]
LEFT_STUNNED = [pygame.image.load('data/models/player/left_stunned_1.png'),
                pygame.image.load('data/models/player/left_stunned_2.png'),
                pygame.image.load('data/models/player/left_stunned_3.png'),
                pygame.image.load('data/models/player/left_stunned_4.png')]
RIGHT_STUNNED = [pygame.image.load('data/models/player/right_stunned_1.png'),
                 pygame.image.load('data/models/player/right_stunned_2.png'),
                 pygame.image.load('data/models/player/right_stunned_3.png'),
                 pygame.image.load('data/models/player/right_stunned_4.png')]
ATTACK_LEFT = [pygame.image.load('data/models/player/left_5.png'),
               pygame.image.load('data/models/player/left_6.png')]
ATTACK_RIGHT = [pygame.image.load('data/models/player/right_5.png'),
                pygame.image.load('data/models/player/right_6.png')]
STANDING = pygame.image.load('data/models/player/stand_1.png')
DEAD = pygame.image.load('data/models/player/die.png')
HEART_IMG = pygame.image.load('data/textures/heart.png')
# Изменение иконки приложения
pygame.display.set_icon(STANDING)
SLIME_RIGHT = [pygame.image.load('data/models/slime/right_1.png'), pygame.image.load('data/models/slime/right_2.png'),
               pygame.image.load('data/models/slime/right_3.png'),
               pygame.image.load('data/models/slime/right_dead.png')]
SLIME_LEFT = [pygame.image.load('data/models/slime/left_1.png'), pygame.image.load('data/models/slime/left_2.png'),
              pygame.image.load('data/models/slime/left_3.png'), pygame.image.load('data/models/slime/left_dead.png')]

FLY_LEFT = [pygame.image.load('data/models/fly/left_1.png'), pygame.image.load('data/models/fly/left_2.png'),
            pygame.image.load('data/models/fly/left_3.png'), pygame.image.load('data/models/fly/left_4.png'),
            pygame.image.load('data/models/fly/left_5.png'), pygame.image.load('data/models/fly/left_6.png'),
            pygame.image.load('data/models/fly/left_dead.png')]
FLY_RIGHT = [pygame.image.load('data/models/fly/right_1.png'), pygame.image.load('data/models/fly/right_2.png'),
             pygame.image.load('data/models/fly/right_3.png'), pygame.image.load('data/models/fly/right_4.png'),
             pygame.image.load('data/models/fly/right_5.png'), pygame.image.load('data/models/fly/right_6.png'),
             pygame.image.load('data/models/fly/right_dead.png')]

SKELETON_LEFT = [pygame.image.load('data/models/skeleton/left_1.png'),
                 pygame.image.load('data/models/skeleton/left_2.png'),
                 pygame.image.load('data/models/skeleton/left_3.png'),
                 pygame.image.load('data/models/skeleton/left_4.png'),
                 pygame.image.load('data/models/skeleton/left_stunned.png')]
SKELETON_ATTACK_LEFT = [pygame.image.load('data/models/skeleton/left_attack_1.png'),
                        pygame.image.load('data/models/skeleton/left_attack_2.png')]
SKELETON_ATTACK_RIGHT = [pygame.image.load('data/models/skeleton/right_attack_1.png'),
                         pygame.image.load('data/models/skeleton/right_attack_2.png')]
SKELETON_RIGHT = [pygame.image.load('data/models/skeleton/right_1.png'),
                  pygame.image.load('data/models/skeleton/right_2.png'),
                  pygame.image.load('data/models/skeleton/right_3.png'),
                  pygame.image.load('data/models/skeleton/right_4.png'),
                  pygame.image.load('data/models/skeleton/right_stunned.png')]
SKELETON_DIE = pygame.image.load('data/models/skeleton/dead.png')

TILE_IMAGE = {'t': pygame.image.load('data/textures/tiles/bt.png'),
              'b': pygame.image.load('data/textures/tiles/bb.png'),
              'l': pygame.image.load('data/textures/tiles/bl.png'),
              'r': pygame.image.load('data/textures/tiles/br.png'),
              'tl': pygame.image.load('data/textures/tiles/btl.png'),
              'tr': pygame.image.load('data/textures/tiles/btr.png'),
              'bl': pygame.image.load('data/textures/tiles/bbl.png'),
              'br': pygame.image.load('data/textures/tiles/bbr.png'),
              'p': pygame.image.load('data/textures/tiles/bp.png'),
              'd': pygame.image.load('data/textures/tiles/bd.png'),
              'spikes': pygame.image.load('data/textures/tiles/spikes.png')}
ENTITY_IMAGE = {'food': pygame.image.load('data/textures/entity/food.png'),
                'potion': pygame.image.load('data/textures/entity/potion.png'),
                'coin': pygame.image.load('data/textures/entity/coin.png')}

# Группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
spikes_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
entity_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

player = None


# Функция загрузки звука
def load_snd(name):
    return pygame.mixer.Sound('data/sfx/' + name + '.wav')


# Загрузка звуков
SOUNDS = {'move': load_snd('move'), 'jump': load_snd('jump'),
          'hurt': load_snd('hurt'), 'smash': load_snd('smash'),
          'squish': load_snd('squish'), 'purchase': load_snd('purchase'),
          'pre_dagger': load_snd('pre_dagger'), 'dagger': load_snd('dagger'),
          'dead_fly': load_snd('dead_fly'), 'skeleton_hit': load_snd('skeleton_hit'),
          'skeleton_dead': load_snd('skeleton_dead'), 'coin': load_snd('coin')}


# Функция загрузки уровня
def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


# Функция вычисления максимальной ширины и высоты уровня
def max_width_height(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))
    max_height = len(list(map(len, level_map)))
    return max_width, max_height


# Функция генерации уровня
def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '0':
                Tile(x, y, 't')
            elif level[y][x] == '1':
                Tile(x, y, 'b')
            elif level[y][x] == '2':
                Tile(x, y, 'l')
            elif level[y][x] == '3':
                Tile(x, y, 'r')
            elif level[y][x] == '4':
                Tile(x, y, 'tl')
            elif level[y][x] == '5':
                Tile(x, y, 'tr')
            elif level[y][x] == '6':
                Tile(x, y, 'bl')
            elif level[y][x] == '7':
                Tile(x, y, 'br')
            elif level[y][x] == '8':
                Tile(x, y, 'p')
            elif level[y][x] == 'd':
                Tile(x, y, 'd')
            elif level[y][x] == '@':
                new_player = Player(x * TILE_WIDTH, y * TILE_WIDTH - 32)
            elif level[y][x] == 's':
                Slime(x, y)
            elif level[y][x] == 'f':
                Fly(x, y)
            elif level[y][x] == 'w':
                SkeletonWarrior(x, y)
            elif level[y][x] == 'x':
                Spikes(x, y)
            elif level[y][x] == 'p':
                Potion(x, y)
            elif level[y][x] == 'c':
                Food(x, y)
            elif level[y][x] == 'n':
                if FILE == LEVELS[0]:
                    Coin(x, y, LEVELS[1])
                elif FILE == LEVELS[1]:
                    Coin(x, y, LEVELS[2])
                elif FILE == LEVELS[2]:
                    Coin(x, y, LEVELS[3])
                else:
                    Coin(x, y, None)

    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


# Функция отрисовки спрайтов
def drawWindow():
    win.blit(bg, (0, 0))
    player.update()
    camera.update(player)
    for e in enemies_group:
        e.update()
    for e in entity_group:
        e.update()
    for e in all_sprites:
        win.blit(e.image, camera.apply(e))
    for i in range(player.health):
        win.blit(HEART_IMG, (10 + i * 16, 10))
    pygame.display.update()


# Функция закрытия приложения
def terminate():
    pygame.quit()
    sys.exit()


# Начальный экран
def start_screen():
    logo = pygame.image.load('data/textures/logo.png')
    press = pygame.image.load('data/textures/press.png')
    made = pygame.image.load('data/textures/made.png')
    count = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        win.fill((0, 0, 0))
        win.blit(logo, (WIDTH // 2 - 969 // 2, HEIGHT // 2 - 100))
        win.blit(made, (WIDTH // 2 - 217 // 2, 650))
        if count < 120:
            if count % 4 == 0:
                win.blit(press, (1280 // 2 - 359 // 2, 500))
            count += 1
        else:
            count = 0
        pygame.display.flip()
        clock.tick(5)


# Экран завершения игры
def end_screen():
    end = pygame.image.load('data/textures/end.png')
    press = pygame.image.load('data/textures/press_quit.png')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                terminate()
        win.fill((0, 0, 0))
        win.blit(end, (WIDTH // 2 - 383 // 2, HEIGHT // 2 - 166 // 2))
        win.blit(press, (WIDTH // 2 - 343 // 2, 600))
        pygame.display.flip()
        clock.tick(60)


def camera_func(camera, target_rect):
    l = -target_rect.x + WIDTH / 2
    t = -target_rect.y + HEIGHT / 2
    w, h = camera.width, camera.height

    l = min(0, l)
    l = max(-(camera.width - WIDTH), l)
    t = max(-(camera.height - HEIGHT), l)
    t = min(0, t)

    return pygame.Rect(l, t, w, h)


# Камера
class Camera:
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


# Персонаж
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = STANDING
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.isMoved = False

        self.left = False
        self.right = True
        self.last_move = 'right'
        self.speed = 8

        self.isAttack = False
        self.slashing = False
        self.attackCount = 0
        self.animCount = 0
        self.isJump = False
        self.isFalling = False
        self.jumpCount = 15
        self.jumpMult = 6

        self.health = 5
        self.isStunned = False
        self.stunCount = 0
        self.dieCount = 0

    def slashing_test(self):
        if self.attackCount // 15 == 1:
            self.slashing = True
        else:
            self.slashing = False

    # Атака
    def attack(self):
        if self.attackCount + 1 >= 30:
            SOUNDS['dagger'].play()
            self.isAttack = False
            self.slashing = False
            if self.isMoved:
                self.rect.x += 34
                self.isMoved = not self.isMoved
            self.attackCount = 0
        elif self.left:
            if self.attackCount // 15 == 1 and not self.isMoved:
                self.rect.x -= 34
                self.isMoved = not self.isMoved
            self.slashing_test()
            self.attackCount += 1
        elif self.right:
            self.slashing_test()
            self.attackCount += 1
        elif self.last_move == 'left':
            if self.attackCount // 15 == 1 and not self.isMoved:
                self.rect.x -= 34
                self.isMoved = not self.isMoved
            self.slashing_test()
            self.attackCount += 1
        elif self.last_move == 'right':
            self.slashing_test()
            self.attackCount += 1

    # Прыжок
    def jump(self):
        if self.jumpCount >= 0:
            self.speed = 12
            self.rect.y -= self.jumpCount ** 2 // self.jumpMult
            if pygame.sprite.spritecollideany(self, tiles_group):
                self.rect.y += self.jumpCount ** 2 // self.jumpMult
                while not pygame.sprite.spritecollideany(self, tiles_group):
                    self.rect.y -= 1
                    if pygame.sprite.spritecollideany(self, tiles_group):
                        self.isJump = False
                        self.jumpCount = 0
                self.rect.y += 1
            else:
                self.jumpCount -= 1
        else:
            self.rect.y += 1
            if not pygame.sprite.spritecollideany(self, tiles_group):
                self.rect.y -= 1
                self.isJump = False
                self.isFalling = True
            else:
                self.rect.y -= 1
                self.isJump = False
                self.speed = 7
                self.jumpCount = 15

    # Падение
    def fall(self):
        self.rect.y += self.jumpCount ** 2 // self.jumpMult
        if pygame.sprite.spritecollideany(self, tiles_group):
            self.rect.y -= self.jumpCount ** 2 // self.jumpMult
            while not pygame.sprite.spritecollideany(self, tiles_group):
                self.rect.y += 1
                if pygame.sprite.spritecollideany(self, tiles_group):
                    self.isFalling = False
                    self.speed = 7
                    self.jumpCount = 15
            self.rect.y -= 1
        else:
            self.jumpCount -= 1

    # Передвижение
    def move(self):
        if not self.isJump and not self.isFalling:
            SOUNDS['move'].play()
            SOUNDS['move'].set_volume(0.1)
        if self.animCount + 1 >= 60:
            self.animCount = 0
        elif self.left:
            player.rect.x -= player.speed
            if pygame.sprite.spritecollideany(player, tiles_group):
                player.rect.x += player.speed
            self.animCount += 1
        elif self.right:
            player.rect.x += player.speed
            if pygame.sprite.spritecollideany(player, tiles_group):
                player.rect.x -= player.speed
            self.animCount += 1

    # Неуязвимость после получения урона
    def stun(self):
        self.attackCount = 0
        self.isAttack = False
        self.slashing = False
        if self.stunCount >= 120:
            self.stunCount = 0
            self.isStunned = False
        elif self.stunCount == 0:
            SOUNDS['hurt'].play()
            self.isStunned = True
            self.stunCount += 1
        else:
            self.stunCount += 1

    # Смерть
    def die(self):
        if self.dieCount >= 60:
            player_group.remove(self)
            all_sprites.remove(self)
        elif self.dieCount == 0:
            self.dieCount += 1
        else:
            self.dieCount += 1

    # Проверка на столкновение с уровнем
    def collide_test_bottom(self):
        self.rect.y += 1
        if not pygame.sprite.spritecollideany(self, tiles_group):
            self.isJump = False
            self.jumpCount = 0
            self.isFalling = True
        elif pygame.sprite.spritecollideany(self, spikes_group) and not self.isStunned:
            self.stun()
            self.isFalling = False
            self.health -= 1
        self.rect.y -= 1

    # Функция обновления положения
    def update(self):
        if self.rect.y >= total_level_height:
            self.health = 0
        if self.health <= 0:
            self.die()
        else:
            if self.animCount + 1 >= 60:
                self.animCount = 0
            if self.left or self.right:
                self.move()
            if self.isStunned:
                self.stun()
            if self.isJump:
                self.jump()
            if self.isFalling:
                self.fall()
            if self.isAttack and not self.isStunned:
                self.attack()
            if not self.isJump and not self.isFalling:
                self.collide_test_bottom()
        self.anim_update()

    # Функция обновления анимации
    def anim_update(self):
        if self.dieCount:
            if self.left:
                self.image = DEAD
            else:
                self.image = DEAD
        elif self.isAttack:
            if self.last_move == 'left':
                self.image = ATTACK_LEFT[self.attackCount // 15]
                self.rect = self.image.get_rect().move(self.rect.x, self.rect.y)
            else:
                self.image = ATTACK_RIGHT[self.attackCount // 15]
                self.rect = self.image.get_rect().move(self.rect.x, self.rect.y)
        elif self.isJump:
            if self.last_move == 'left':
                if self.isStunned:
                    self.image = LEFT_STUNNED[1]
                else:
                    self.image = LEFT_MOVE[1]
            else:
                if self.isStunned:
                    self.image = RIGHT_STUNNED[1]
                else:
                    self.image = RIGHT_MOVE[1]
        elif self.isFalling:
            if self.last_move == 'left':
                if self.isStunned:
                    self.image = LEFT_STUNNED[3]
                else:
                    self.image = LEFT_MOVE[3]
            else:
                if self.isStunned:
                    self.image = RIGHT_STUNNED[3]
                else:
                    self.image = RIGHT_MOVE[3]
        elif self.left:
            if self.isStunned:
                self.image = LEFT_STUNNED[self.animCount // 15]
                self.rect = RIGHT_MOVE[3].get_rect().move(self.rect.x, self.rect.y)
            else:
                self.image = LEFT_MOVE[self.animCount // 15]
                self.rect = RIGHT_MOVE[3].get_rect().move(self.rect.x, self.rect.y)
        elif self.right:
            if self.isStunned:
                self.image = RIGHT_STUNNED[self.animCount // 15]
                self.rect = RIGHT_MOVE[3].get_rect().move(self.rect.x, self.rect.y)
            else:
                self.image = RIGHT_MOVE[self.animCount // 15]
                self.rect = RIGHT_MOVE[3].get_rect().move(self.rect.x, self.rect.y)
        elif self.last_move == 'left':
            if self.isStunned:
                self.image = LEFT_STUNNED[0]
                self.rect = RIGHT_MOVE[3].get_rect().move(self.rect.x, self.rect.y)
            else:
                self.image = LEFT_MOVE[0]
                self.rect = RIGHT_MOVE[3].get_rect().move(self.rect.x, self.rect.y)
        elif self.last_move == 'right':
            if self.isStunned:
                self.image = RIGHT_STUNNED[0]
                self.rect = RIGHT_MOVE[3].get_rect().move(self.rect.x, self.rect.y)
            else:
                self.image = RIGHT_MOVE[0]
                self.rect = RIGHT_MOVE[3].get_rect().move(self.rect.x, self.rect.y)


# Слизень
class Slime(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(enemies_group, all_sprites)
        self.image = SLIME_LEFT[0]
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x, TILE_WIDTH * pos_y)

        self.standCount = 0
        self.speed = 7
        self.left = True
        self.right = False

        self.animCount = 0
        self.isJump = False
        self.isFalling = False
        self.jumpCount = 15
        self.jumpMult = 16

        self.health = 1
        self.dieCount = 0

    # Столлкновения с персонажем
    def kick(self):
        if self.rect.x > player.rect.x and player.last_move == 'right' and player.slashing:
            self.health -= 1
        elif self.rect.x < player.rect.x and player.last_move == 'left' and player.slashing:
            self.health -= 1
        elif not player.isStunned and self.health > 0:
            player.stun()
            player.health -= 1

    # Смерть
    def die(self):
        if self.dieCount >= 60:
            enemies_group.remove(self)
            all_sprites.remove(self)
        elif self.dieCount == 0:
            SOUNDS['squish'].play()
            if self.left:
                self.image = SLIME_LEFT[-1]
            else:
                self.image = SLIME_RIGHT[-1]
            self.dieCount += 1
        else:
            if self.left:
                self.image = SLIME_LEFT[-1]
            else:
                self.image = SLIME_RIGHT[-1]
            self.dieCount += 1

    # Передвижение
    def move(self):
        if self.left:
            self.rect.x -= self.speed
            if pygame.sprite.spritecollideany(self, tiles_group):
                self.rect.x += self.speed
                while not pygame.sprite.spritecollideany(self, tiles_group):
                    self.rect.x -= 1
                    if pygame.sprite.spritecollideany(self, tiles_group):
                        self.right = True
                        self.left = False
                self.rect.x += 1
        elif self.right:
            self.rect.x += self.speed
            if pygame.sprite.spritecollideany(self, tiles_group):
                self.rect.x -= self.speed
                while not pygame.sprite.spritecollideany(self, tiles_group):
                    self.rect.x += 1
                    if pygame.sprite.spritecollideany(self, tiles_group):
                        self.right = False
                        self.left = True
                self.rect.x -= 1

    # Проверка на столкновение с уровнем
    def collide_test_bottom(self):
        self.rect.y += 1
        if not pygame.sprite.spritecollideany(self, tiles_group):
            self.rect.y -= 1
            self.isJump = False
            self.isFalling = True
        elif pygame.sprite.spritecollideany(self, spikes_group):
            self.isFalling = False
            self.health -= 1
        else:
            self.rect.y -= 1
            self.isJump = False
            self.speed = 7
            self.jumpCount = 15

    # Прыжок
    def jump(self):
        if self.jumpCount >= 0:
            self.rect.y -= self.jumpCount ** 2 // self.jumpMult
            self.move()
            if pygame.sprite.spritecollideany(self, tiles_group):
                self.rect.y += self.jumpCount ** 2 // self.jumpMult
                while not pygame.sprite.spritecollideany(self, tiles_group):
                    self.rect.y -= 1
                    if pygame.sprite.spritecollideany(self, tiles_group):
                        self.isJump = False
                        self.jumpCount = 0
                self.rect.y += 1
            else:
                self.jumpCount -= 1
        else:
            self.collide_test_bottom()

    # Падение
    def fall(self):
        self.rect.y += self.jumpCount ** 2 // self.jumpMult
        self.move()
        if pygame.sprite.spritecollideany(self, tiles_group):
            self.rect.y -= self.jumpCount ** 2 // self.jumpMult
            while not pygame.sprite.spritecollideany(self, tiles_group):
                self.rect.y += 1
                if pygame.sprite.spritecollideany(self, tiles_group):
                    self.isFalling = False
                    self.speed = 7
                    self.jumpCount = 15
            self.rect.y -= 1
        else:
            self.jumpCount -= 1

    # Функция обновления
    def update(self):
        if self.rect.y >= total_level_height:
            self.health = 0
        if pygame.sprite.spritecollideany(self, player_group):
            self.kick()
        if self.health <= 0:
            if not self.dieCount:
                SOUNDS['squish'].play()
            self.die()
        else:
            if self.standCount < 60 and not self.isJump and not self.isFalling:
                self.standCount += 1
            else:
                self.standCount = 0
                self.isJump = True
            if self.isJump:
                self.jump()
            if self.isFalling:
                self.fall()
            if not self.isJump and not self.isFalling:
                self.collide_test_bottom()
        self.anim_update()

    def anim_update(self):
        if self.dieCount:
            if self.left:
                self.image = SLIME_LEFT[-1]
            else:
                self.image = SLIME_RIGHT[-1]
        elif self.standCount < 60 and not self.isJump and not self.isFalling:
            if self.left:
                self.image = SLIME_LEFT[self.standCount // 20]
            else:
                self.image = SLIME_RIGHT[self.standCount // 20]


# Летающий моб
class Fly(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(enemies_group, all_sprites)
        self.image = FLY_LEFT[0]
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x, TILE_WIDTH * pos_y)

        self.speed = 2
        self.left = True
        self.right = False

        self.animCount = 0
        self.isFalling = False
        self.jumpCount = 0

        self.health = 1
        self.dieCount = 0

    # Столлкновения с персонажем
    def kick(self):
        if self.rect.x > player.rect.x and player.last_move == 'right' and player.slashing:
            self.health -= 1
        elif self.rect.x < player.rect.x and player.last_move == 'left' and player.slashing:
            self.health -= 1
        elif not player.isStunned and not self.dieCount:
            player.stun()
            player.health -= 1

    # Смерть
    def die(self):
        if self.dieCount >= 60:
            enemies_group.remove(self)
            all_sprites.remove(self)
        elif self.dieCount == 0:
            SOUNDS['dead_fly'].play()
            self.dieCount += 1
        else:
            self.dieCount += 1

    # Передвижение
    def move(self):
        if self.left:
            self.rect.x -= self.speed
            if pygame.sprite.spritecollideany(self, tiles_group):
                self.rect.x += self.speed
                while not pygame.sprite.spritecollideany(self, tiles_group):
                    self.rect.x -= 1
                    if pygame.sprite.spritecollideany(self, tiles_group):
                        self.right = True
                        self.left = False
                self.rect.x += 1
        elif self.right:
            self.rect.x += self.speed
            if pygame.sprite.spritecollideany(self, tiles_group):
                self.rect.x -= self.speed
                while not pygame.sprite.spritecollideany(self, tiles_group):
                    self.rect.x += 1
                    if pygame.sprite.spritecollideany(self, tiles_group):
                        self.right = False
                        self.left = True
                self.rect.x -= 1

    # Падение
    def fall(self):
        self.rect.y += self.jumpCount ** 2 // 24
        self.move()
        if pygame.sprite.spritecollideany(self, tiles_group):
            self.rect.y -= self.jumpCount ** 2 // 24
            while not pygame.sprite.spritecollideany(self, tiles_group):
                self.rect.y += 1
                if pygame.sprite.spritecollideany(self, tiles_group):
                    self.isFalling = False
                    self.jumpCount = 0
            self.rect.y -= 1
        else:
            self.jumpCount -= 1

    # Проверка на столкновение с уровнем
    def collide_test_bottom(self):
        self.rect.y += 1
        if not pygame.sprite.spritecollideany(self, tiles_group):
            self.rect.y -= 1
            self.isFalling = True
        else:
            self.rect.y -= 1

    # Проверка столкновения с уровнем по горизонтали
    def collide_test_x(self):
        if self.left:
            self.rect.x -= self.rect[2]
            self.rect.y += 1
            if not pygame.sprite.spritecollideany(self, tiles_group):
                self.left = False
                self.right = True
            self.rect.x += self.rect[2]
            self.rect.y -= 1
        else:
            self.rect.x += self.rect[2]
            self.rect.y += 1
            if not pygame.sprite.spritecollideany(self, tiles_group):
                self.left = True
                self.right = False
            self.rect.x -= self.rect[2]
            self.rect.y -= 1

    # Функция обновления
    def update(self):
        self.collide_test_x()
        if pygame.sprite.spritecollideany(self, player_group):
            self.kick()
        if self.health <= 0:
            self.die()
        else:
            if self.animCount < 60:
                self.move()
                self.animCount += 1
            else:
                self.animCount = 0
            if self.isFalling:
                self.fall()
            if not self.isFalling:
                self.collide_test_bottom()
        self.anim_update()

    def anim_update(self):
        if self.dieCount:
            if self.left:
                self.image = FLY_LEFT[-1]
            else:
                self.image = FLY_RIGHT[-1]
        elif self.animCount < 60:
            if self.left:
                self.image = FLY_LEFT[self.animCount // 10]
            else:
                self.image = FLY_RIGHT[self.animCount // 10]


# Скелет-воин
class SkeletonWarrior(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(enemies_group, all_sprites)
        self.image = SKELETON_LEFT[0]
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x, TILE_WIDTH * pos_y)

        self.standCount = 0
        self.speed = 2
        self.left = True
        self.right = False
        self.triggered = False
        self.isAttack = False
        self.slashing = False
        self.isMoved = False

        self.attackCount = 0
        self.animCount = 0
        self.isFalling = False
        self.jumpCount = 0

        self.health = 3
        self.dieCount = 0
        self.isStunned = False
        self.stunCount = 0

    # Передвижение
    def move(self):
        if self.animCount < 60:
            if self.left:
                self.rect.x -= self.speed
                if pygame.sprite.spritecollideany(self, tiles_group):
                    self.rect.x += self.speed
                    while not pygame.sprite.spritecollideany(self, tiles_group):
                        self.rect.x -= 1
                        if pygame.sprite.spritecollideany(self, tiles_group):
                            self.right = True
                            self.left = False
                    self.rect.x += 1
            else:
                self.rect.x += self.speed
                if pygame.sprite.spritecollideany(self, tiles_group):
                    self.rect.x -= self.speed
                    while not pygame.sprite.spritecollideany(self, tiles_group):
                        self.rect.x += 1
                        if pygame.sprite.spritecollideany(self, tiles_group):
                            self.right = False
                            self.left = True
                    self.rect.x -= 1
            self.animCount += 1
        else:
            self.animCount = 0

    # Неуязвимость после получения урона
    def stun(self):
        self.triggered = False
        self.attackCount = 0
        self.isAttack = False
        if self.stunCount >= 60:
            self.stunCount = 0
            self.isStunned = False
            self.speed = 2
        elif self.stunCount == 0:
            self.speed = 0
            self.isStunned = True
            self.stunCount += 1
        else:
            self.stunCount += 1

    # Столкновение с персонажем
    def kick(self):
        if self.rect.x > player.rect.x and not self.isStunned and not self.slashing and \
                player.last_move == 'right' and player.slashing:
            SOUNDS['skeleton_hit'].play()
            self.health -= 1
            self.stun()
        elif self.rect.x < player.rect.x and not self.isStunned and not self.slashing and \
                player.last_move == 'left' and player.slashing:
            SOUNDS['skeleton_hit'].play()
            self.health -= 1
            self.stun()
        elif self.slashing and not player.isStunned and pygame.sprite.spritecollideany(self, player_group):
            player.stun()
            player.health -= 1

    # Смерть
    def die(self):
        if self.dieCount >= 60:
            enemies_group.remove(self)
            all_sprites.remove(self)
        elif self.dieCount == 0:
            SOUNDS['skeleton_dead'].play()
            self.dieCount += 1
        else:
            self.dieCount += 1

    def slashing_test(self):
        if self.image == SKELETON_ATTACK_LEFT[-1] or self.image == SKELETON_ATTACK_RIGHT[-1]:
            self.slashing = True
        else:
            self.slashing = False

    # Атака
    def attack(self):
        if self.attackCount + 1 >= 60:
            self.isAttack = False
            self.slashing = False
            if self.isMoved:
                if self.left:
                    self.rect.x += 34
                else:
                    self.rect.x -= 34
                self.isMoved = not self.isMoved
            self.speed = 2
            self.attackCount = 0
        elif self.left:
            self.speed = 0
            if self.attackCount // 30 == 1 and not self.isMoved:
                self.rect.x -= 34
                self.isMoved = not self.isMoved
            self.slashing_test()
            self.attackCount += 1
        elif self.right:
            self.speed = 0
            if self.attackCount // 30 == 1 and not self.isMoved:
                self.rect.x += 34
                self.isMoved = not self.isMoved
            self.slashing_test()
            self.attackCount += 1

    # Падение
    def fall(self):
        self.rect.y += self.jumpCount ** 2 // 6
        if pygame.sprite.spritecollideany(self, tiles_group):
            self.rect.y -= self.jumpCount ** 2 // 6
            while not pygame.sprite.spritecollideany(self, tiles_group):
                self.rect.y += 1
                if pygame.sprite.spritecollideany(self, tiles_group):
                    self.isFalling = False
                    self.jumpCount = 0
            self.rect.y -= 1
        else:
            self.jumpCount -= 1

    # Проверка на столкновение с уровнем
    def collide_test_bottom(self):
        self.rect.y += 1
        if not pygame.sprite.spritecollideany(self, tiles_group):
            self.jumpCount = 0
            self.isFalling = True
        self.rect.y -= 1

    # Проверка на столкновение с уровнем по горизонтали
    def collide_test_x(self):
        if self.left:
            self.rect.x -= self.rect[2]
            self.rect.y += 1
            if not pygame.sprite.spritecollideany(self, tiles_group):
                self.left = False
                self.right = True
            self.rect.x += self.rect[2]
            self.rect.y -= 1
        else:
            self.rect.x += self.rect[2]
            self.rect.y += 1
            if not pygame.sprite.spritecollideany(self, tiles_group):
                self.left = True
                self.right = False
            self.rect.x -= self.rect[2]
            self.rect.y -= 1

    # Проверка на тирггер
    def trigger_test(self):
        if fabs(self.rect.x - player.rect.x) <= 70 and fabs(self.rect.y - player.rect.y) <= 50 and not player.isStunned:
            self.triggered = True
            self.isAttack = True
        else:
            self.triggered = False

    # Функция обновления
    def update(self):
        self.trigger_test()
        if not self.triggered and not self.isAttack:
            self.collide_test_x()
            if pygame.sprite.spritecollideany(self, player_group):
                self.kick()
            if self.health <= 0:
                self.die()
            else:
                if self.left or self.right:
                    self.move()
                if self.isFalling:
                    self.fall()
                if self.isStunned:
                    self.stun()
                if not self.isFalling:
                    self.collide_test_bottom()
        else:
            if self.rect.x < player.rect.x:
                self.left = False
                self.right = True
            elif self.rect.x > player.rect.x:
                self.left = True
                self.right = False
            if self.isStunned:
                self.stun()
            if pygame.sprite.spritecollideany(self, player_group):
                self.kick()
            if self.isAttack and not self.isStunned:
                self.attack()
                self.kick()
            if self.health <= 0:
                self.die()
        self.anim_update()

    def anim_update(self):
        if self.dieCount:
            if self.left:
                self.image = SKELETON_DIE
            else:
                self.image = SKELETON_DIE
        elif self.stunCount:
            if self.left:
                self.image = SKELETON_LEFT[-1]
            else:
                self.image = SKELETON_RIGHT[-1]
        elif self.isAttack:
            if self.left:
                self.image = SKELETON_ATTACK_LEFT[self.attackCount // 30]
                self.rect = self.image.get_rect().move(self.rect.x, self.rect.y)
            else:
                self.image = SKELETON_ATTACK_RIGHT[self.attackCount // 30]
                self.rect = self.image.get_rect().move(self.rect.x, self.rect.y)
        else:
            if self.left:
                self.image = SKELETON_LEFT[self.animCount // 15]
            else:
                self.image = SKELETON_RIGHT[self.animCount // 15]


# Плитка
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, type):
        super().__init__(tiles_group, all_sprites)
        self.image = TILE_IMAGE[type]
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x, TILE_WIDTH * pos_y)


# Шипы
class Spikes(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(spikes_group, all_sprites)
        self.image = TILE_IMAGE['spikes']
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x, TILE_WIDTH * pos_y)


# Еда
class Food(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(entity_group, all_sprites)
        self.image = ENTITY_IMAGE['food']
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x, TILE_WIDTH * pos_y)

    # Повышает уровень здоровья на 1 единицу, если здоровье персонажа меньше 5 единиц
    def update(self):
        if pygame.sprite.spritecollideany(self, player_group) and player.health < 5:
            SOUNDS['squish'].play()
            player.health += 1
            entity_group.remove(self)
            all_sprites.remove(self)


# Зелье
class Potion(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(entity_group, all_sprites)
        self.image = ENTITY_IMAGE['potion']
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x, TILE_WIDTH * pos_y)

    # Повышает уровень здоровья на 3 единицы
    def update(self):
        if pygame.sprite.spritecollideany(self, player_group):
            SOUNDS['purchase'].play()
            player.health += 3
            entity_group.remove(self)
            all_sprites.remove(self)


# Монета
class Coin(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, filename):
        super().__init__(entity_group, all_sprites)
        self.image = ENTITY_IMAGE['coin']
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x, TILE_WIDTH * pos_y)
        self.filename = filename

    # Переход на следующий уровень
    def update(self):
        if pygame.sprite.spritecollideany(self, player_group):
            SOUNDS['coin'].play()
            global FILE, running
            if self.filename:
                FILE = self.filename
            else:
                running = False
            entity_group.remove(self)
            all_sprites.remove(self)
            player.health = 0
            player.dieCount = 60


# Вызыв начального экрана
start_screen()

# Генерпция уровня
player, level_x, level_y = generate_level(load_level(FILE))

max_width, max_height = max_width_height(FILE)

total_level_width = max_width * TILE_WIDTH
total_level_height = max_height * TILE_WIDTH

# Создание камеры
camera = Camera(camera_func, total_level_width, total_level_height)

# Загрузка и воспроизведение саундтрека
pygame.mixer.music.load('data/music/main.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

# Игровой цикл
running = True
while running:
    clock.tick(FPS)
    # Если персонаж умер, очищаем все группы спрайтов и генерируем уровень заново
    if not player_group:
        for e in all_sprites:
            all_sprites.remove(e)
        for e in tiles_group:
            tiles_group.remove(e)
        for e in spikes_group:
            spikes_group.remove(e)
        for e in enemies_group:
            enemies_group.remove(e)
        for e in entity_group:
            entity_group.remove(e)
        for e in player_group:
            player_group.remove(e)
        player, level_x, level_y = generate_level(load_level(FILE))
        max_width, max_height = max_width_height(FILE)

        total_level_width = max_width * TILE_WIDTH
        total_level_height = max_height * TILE_WIDTH

        camera = Camera(camera_func, total_level_width, total_level_height)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.rect.x > 0:
        player.left = True
        player.right = False
        player.last_move = 'left'
    elif keys[pygame.K_RIGHT]:
        player.left = False
        player.right = True
        player.last_move = 'right'
    else:
        player.left = False
        player.right = False
        player.animCount = 0
    if not player.isJump and not player.isFalling:
        if keys[pygame.K_SPACE]:
            SOUNDS['jump'].play()
            player.isJump = True
    if not player.isAttack and not player.isStunned:
        if keys[pygame.K_x]:
            SOUNDS['pre_dagger'].play()
            player.isAttack = True
    drawWindow()

# Вызов экрана завершения игры
end_screen()
pygame.quit()
