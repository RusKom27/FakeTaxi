import os
import sys
import webbrowser

import pygame
import random
from pygame import mixer

# переменные для конфигурации игры
WIDTH = 1200
HEIGHT = 700
FPS = 60

# переменные цветовых кодов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


# метод для безопасной загрузки в системе
def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


# инициализация элементов движка
pygame.init()
pygame.mixer.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fake Taxi")
clock = pygame.time.Clock()


running = True

class Road:
    def __init__(self, x=370, y=0, angle=0):
        self.image = storage.road_image
        self.orig_image = self.image
        self.rect = (x,y,storage.road_rect.width,storage.road_rect.height)
        self.angle = angle

    def update(self):
        self.rotate()

    def draw(self):
        screen.blit(self.image, self.rect)

    def rotate(self):
        self.image = pygame.transform.rotozoom(self.orig_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

class Roads:
    def __init__(self):
        self.roads = [Road(y=0,angle=0), Road(y=320,angle=0)]
        self.angle = 0

    def update(self):
        for road in self.roads:
            if self.angle > 360:
                self.angle = 0
            self.angle += 0.1
            road.angle = self.angle
            road.update()

    def draw(self):
        for road in self.roads:
            road.draw()


class Storage:
    def __init__(self):
        self.player_image = load_image("player", 46, 102)
        self.player_rect = self.player_image.get_rect()

        self.road_image = load_image("road", 520, 520)
        self.road_rect = self.road_image.get_rect()

class GameManager:
    def __init__(self):
        self.in_game = True
        self.in_pause = False

    def update(self):
        if self.in_game:
            roads.update()
        if self.in_pause:
            pass

    def draw(self):
        if self.in_game:
            roads.draw()
        if self.in_pause:
            pass


def animation(Entity, images, speed, endless):
    now = pygame.time.get_ticks()
    is_alive = True
    if now - Entity.last_sprite_update > speed:
        Entity.i += 1
        if Entity.i > len(images) - 1:
            if endless:
                Entity.i = 0
            else:
                Entity.i = 0
                try:
                    Entity.kill()
                except Exception:
                    pass
                is_alive = False
                return is_alive
        if is_alive:
            Entity.last_sprite_update = now
            new_image = images[Entity.i]
            Entity.image = new_image

def mouse_in_rect(rect):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    return rect.left < mouse_x < rect.left + rect.width and rect.top < mouse_y < rect.top + rect.height

def load_image(name, scaleX, scaleY):
    try:
        return pygame.transform.scale(
            pygame.image.load(resource_path(os.path.join("venv\\Sprites\\", str(name) + ".png"))).convert_alpha(),(scaleX, scaleY))
    except Warning:
        print(Warning)

def load_images(name, count, scaleX, scaleY):
    array = []
    for i in range(count):
        array.append(load_image(str(name) + str(i + 1), scaleX, scaleY))
    return array

storage = Storage()

roads = Roads()
game_manager = GameManager()


while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    game_manager.update()
    game_manager.draw()
    pygame.display.flip()
sys.exit()