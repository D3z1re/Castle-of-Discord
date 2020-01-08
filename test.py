import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 487
win = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Castle of Discord')

LEFT_MOVE = [pygame.image.load('left_1.png'), pygame.image.load('left_2.png'),
             pygame.image.load('left_3.png'), pygame.image.load('left_4.png'),
             pygame.image.load('left_5.png'), pygame.image.load('left_6.png')]

RIGHT_MOVE = [pygame.image.load('right_1.png'), pygame.image.load('right_2.png'),
              pygame.image.load('right_3.png'), pygame.image.load('right_4.png'),
              pygame.image.load('right_5.png'), pygame.image.load('right_6.png')]

STANDING = [pygame.image.load('stand_1.png'), pygame.image.load('stand_2.png'),
            pygame.image.load('stand_3.png'), pygame.image.load('stand_4.png'),
            pygame.image.load('stand_5.png'), pygame.image.load('stand_6.png')]

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
boxes_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

player = None


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = STANDING[0]
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.left = False
        self.right = True
        self.animCount = 0
        self.isJump = False
        self.jumpCount = 10

        if self.animCount + 1 >= 60:
            self.animCount = 0
        if left:
            win.blit(LEFT_MOVE[self.animCount // 10], (x, y))
            self.animCount += 1
        elif right:
            win.blit(RIGHT_MOVE[self.animCount // 10], (x, y))
            self.animCount += 1
        else:
            win.blit(STANDING[self.animCount // 10], (x, y))


def drawWindow():
    global animCount
    win.blit(bg, (0, 0))

    if animCount + 1 >= 60:
        animCount = 0
    if left:
        win.blit(LEFT_MOVE[animCount // 10], (x, y))
        animCount += 1
    elif right:
        win.blit(RIGHT_MOVE[animCount // 10], (x, y))
        animCount += 1
    else:
        win.blit(STANDING[animCount // 10], (x, y))
    all_sprites.draw(win)
    pygame.display.update()


x = 50
y = 320
width = 256
height = 192
speed = 7
isJump = False
jumpCount = 10

bg = pygame.image.load('bg.png')

left = False
right = False
animCount = 0
player = Player(100, 300)

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x > 5:
        x -= speed
        left = True
        right = False
        player.rect.x -= speed
        player.left = True
        player.right = False
    elif keys[pygame.K_RIGHT]and x < WIDTH - (width // 2):
        x += speed
        player.rect.x += speed
        player.left = False
        player.right = True
        left = False
        right = True
    else:
        left = False
        right = False

        animCount = 0
    if not player.isJump:
        if keys[pygame.K_SPACE]:
            isJump = True
            player.isJump = True
    else:
        if player.jumpCount >= -10:
            if jumpCount < 0:
                y += jumpCount ** 2 / 2
                player.rect.y = player.jumpCount ** 2 / 2
            else:
                y -= jumpCount ** 2 / 2
                player.rect.y = jumpCount ** 2 / 2
            jumpCount -= 1
            player.jumpCount -= 1
        else:
            isJump = False
            player.isJump = False
            jumpCount = 10
            player.jumpCount = 10
    drawWindow()
pygame.quit()
