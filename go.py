import pygame
import random
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
from os import listdir

FPS = pygame.time.Clock()

PINK = (255, 25, 255)
RED = (255, 0, 0)
GREEN = (34, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
screen = width, height = 800, 600
main_surface = pygame.display.set_mode(screen)
IMG_PATH = 'goose'
ball_img = [pygame.image.load(IMG_PATH + '/' + file).convert_alpha() for file in listdir(IMG_PATH)]
img_index = 0

ball = ball_img[img_index]
ball_rect = ball.get_rect()
ball_speed = 5

lives = 3
scores = 0
font = pygame.font.SysFont('Arial', 30, True)
delay = 500
bg = pygame.transform.scale(pygame.image.load('background.png').convert(), screen)
bg_x = 0
bg_x2 = bg.get_width()
bg_speed = 3


def create_enemy():
    enemy = pygame.transform.scale(pygame.image.load('enemy.png').convert_alpha(), (80, 50))
    enemy_rect = pygame.Rect(width, random.randint(0, height - enemy.get_height()), *enemy.get_size())
    enemy_speed = random.randint(2, 5)
    return [enemy, enemy_rect, enemy_speed]


def create_bonus():
    bonus = pygame.transform.scale(pygame.image.load('bonus.png').convert_alpha(), (80, 100))
    bonus_rect = pygame.Rect(random.randint(0, width - bonus.get_width()), 0, *bonus.get_size())
    bonus_speed = random.randint(2, 5)
    return [bonus, bonus_rect, bonus_speed]


enemies = []
bonuses = []
CRATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CRATE_ENEMY, 1500)

CRATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CRATE_BONUS, 2500)

CHANGE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 125)

is_working = True

while is_working:
    FPS.tick(60)
    if lives < 0:
        is_working = False
    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
        if event.type == CRATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CRATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMG:
            img_index += 1
            if img_index == len(ball_img):
                img_index = 0
        ball = ball_img[img_index]

    bg_x -= bg_speed
    bg_x2 -= bg_speed

    if bg_x < -bg.get_width():
        bg_x = bg.get_width()
    if bg_x2 < -bg.get_width():
        bg_x2 = bg.get_width()

    main_surface.blit(bg, (bg_x, 0))
    main_surface.blit(bg, (bg_x2, 0))
    main_surface.blit(ball, ball_rect)
    main_surface.blit(font.render("Scores " + str(scores), True, GREEN), (width - 130, 0))
    main_surface.blit(font.render("Lives " + str(lives), True, GREEN), (width - 130, 30))

    for enemy in enemies:
        main_surface.blit(enemy[0], enemy[1])
        enemy[1] = enemy[1].move(-enemy[2], 0)
        if ball_rect.colliderect(enemy[1]):
            enemies.pop(enemies.index(enemy))
            lives -= 1
        if not lives:
            delay -= 1
            main_surface.blit(font.render("GAME OVER", True, RED), (300, 300))
            if not delay:
                is_working = False
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        main_surface.blit(bonus[0], bonus[1])
        bonus[1] = bonus[1].move(0, bonus[2])
        if ball_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            scores += 1
        if bonus[1].bottom > height:
            bonuses.pop(bonuses.index(bonus))

    pressed_keys = pygame.key.get_pressed()

    if pressed_keys[K_DOWN] and not ball_rect.bottom >= height:
        ball_rect = ball_rect.move(0, ball_speed)
    if pressed_keys[K_UP] and not ball_rect.top <= 0:
        ball_rect = ball_rect.move(0, -ball_speed)
    if pressed_keys[K_LEFT] and not ball_rect.left <= 0:
        ball_rect = ball_rect.move(-ball_speed, 0)
    if pressed_keys[K_RIGHT] and not ball_rect.right >= width:
        ball_rect = ball_rect.move(ball_speed, 0)

    pygame.display.flip()
