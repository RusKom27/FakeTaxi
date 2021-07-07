import os
import sys

import pygame
import random

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
pygame.font.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fake Taxi")
clock = pygame.time.Clock()

running = True


# Класс машины, от нее будет наследоваться класс игрока и другие машины
class Car(pygame.sprite.Sprite):
    def __init__(self, speed, images, dir):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        if dir == 1:
            for image in images:
                self.images.append(pygame.transform.rotate(image, 180))
        elif dir == 0:
            self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect()

        self.last_sprite_update = pygame.time.get_ticks()
        self.i = 0
        self.speed = speed


# Класс игрока (отрисовка, передвижение)
class Player(Car):
    def __init__(self):
        super().__init__(0, storage.taxi_images, 0)
        self.speedx = 0
        self.speedy = 0
        self.rect.x = 610
        self.rect.y = 300
        self.rect.height -= 50

    def update(self):
        self.speed = 4 * game_manager.game_speed
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if any(keystate):
            if keystate[pygame.K_LEFT]:
                animation(self, self.images, 200, True, 5)
                gamebox.joystick_image = storage.joystick_images[4]
                self.speedx = -1 * self.speed
            elif keystate[pygame.K_RIGHT]:
                animation(self, self.images, 200, True, -5)
                gamebox.joystick_image = storage.joystick_images[3]
                self.speedx = self.speed
            if keystate[pygame.K_UP]:
                gamebox.joystick_image = storage.joystick_images[1]
                self.speedy = -1 * self.speed
            elif keystate[pygame.K_DOWN]:
                gamebox.joystick_image = storage.joystick_images[2]
                self.speedy = self.speed
        else:
            gamebox.joystick_image = storage.joystick_images[0]
            animation(self, self.images, 200, True)

        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.x > 865:
            self.rect.x = 865
        if self.rect.x < 253:
            self.rect.x = 253
        if self.rect.y < 25:
            self.rect.y = 25
        if self.rect.y > 260:
            self.rect.y = 260

    def draw(self):
        screen.blit(self.image, self.rect)


# Класс других машин (отрисовка, отслеживание коллизий, передвижение)
class TrafficCar(Car):
    def __init__(self, dir, x, y=-100):
        self.dir = dir
        if dir == 0 or dir == 1:
            super().__init__(0, storage.cars_images[random.randint(0, 3)], 1)
        elif dir == 2 or dir == 3:
            super().__init__(0, storage.cars_images[random.randint(0, 3)], 0)
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.dir == 0 or self.dir == 1:
            self.speed = 6 * game_manager.game_speed
        elif self.dir == 2 or self.dir == 3:
            self.speed = 2 * game_manager.game_speed
        self.rect.y += self.speed
        animation(self, self.images, 200, True)
        if self.rect.y > 800:
            all_cars.remove(self)
        if self.rect.colliderect(player.rect):
            game_manager.in_pause = True
            game_manager.in_game = False
            score_board.scores = 0
            player.rect.x = 610
            player.rect.y = 300
            self.kill()


# Класс спавнера машин (рандомное создание машин и назначение параметров в зависимости от координат машины)
class Traffic:
    def __init__(self):
        self.coords = [400, 500, 615, 725]
        self.last_update = pygame.time.get_ticks()
        self.speed = 4000

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.speed:
            place = random.randint(0, 1)
            car = TrafficCar(place, x=self.coords[place], y=random.randint(300, 350) * -1)
            all_cars.add(car)
            place = random.randint(2, 3)
            car = TrafficCar(place, x=self.coords[place], y=random.randint(300, 350) * -1)
            all_cars.add(car)
            self.last_update = now


# Класс человека (в зависимости от параметров обретает характерные свойства типа скорости, поворот, положение, координаты)
class Human(pygame.sprite.Sprite):
    def __init__(self, images, state=0, dir=0):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.last_sprite_update = pygame.time.get_ticks()
        self.i = 0
        if dir == 1:
            for image in images:
                self.images.append(pygame.transform.rotate(image, 180))
            self.speed = 6 * game_manager.game_speed
        elif dir == 0:
            self.images = images
            self.speed = 4 * game_manager.game_speed
        if state == 0:
            self.images = self.images[:-2]
            self.image = self.images[0]
            self.rect = self.image.get_rect()
            self.rect.x = random.randint(210, 275) + (620 * random.randint(0, 1))
        elif state == 1:
            self.image = self.images[-1]
            self.rect = self.image.get_rect()
            self.rect.x = 300 + (500 * dir)
            self.speed = 5 * game_manager.game_speed
        self.rect.y = -100
        self.state = state
        self.dir = dir

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.kill()
        if self.rect.colliderect(player.rect):
            if self.state == 1:
                if self.dir == 1:
                    score_board.scores += 1
                elif self.dir == 0:
                    score_board.scores += 2
                self.kill()
            if self.state == 0:
                game_manager.in_pause = True
                game_manager.in_game = False
                score_board.scores = 0
                player.rect.x = 610
                player.rect.y = 300
                self.kill()
        if self.state == 0:
            animation(self, self.images, 200, True)


# Спавнер людей (назначение положения и координат)
class Humans:
    def __init__(self):
        self.speed = 500
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.speed:
            human = Human(images=storage.humans_images[random.randint(0, 11)],
                          state=random.randint(0, 1) * random.randint(0, 1), dir=random.randint(0, 1))
            all_humans.add(human)
            self.last_update = now


# Класс дороги (передвижение, отрисовка)
class Road(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, type = 0):
        pygame.sprite.Sprite.__init__(self)
        self.image = storage.road_images[type]
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
        self.speed = 5 * game_manager.game_speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 450:
            self.rect.y = -400

    def draw(self):
        screen.blit(self.image, self.rect)


# Класс подсчета очков и отображения на экране
class ScoreBoard:
    def __init__(self):
        self.scores = 0

    def draw(self):
        print_text(f"SCORES: {self.scores}", storage.font25, WHITE, 250, 50)


class GameBox(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = storage.gamebox_images[0]
        self.rect = self.image.get_rect()
        self.last_sprite_update = pygame.time.get_ticks()
        self.i = 0

        self.joystick_image = storage.joystick_images[0]
        self.joystick_rect = self.joystick_image.get_rect()
        self.joystick_rect.x = 239
        self.joystick_rect.y = 470

        self.start_button = Button(storage.buttonred_images,860, 500,self.start_or_pause)
        self.exit_button = Button(storage.buttonblue_images, 898, 600, self.exit)



    def update(self):
        self.start_button.update()
        self.exit_button.update()
        animation(self, storage.gamebox_images, 200, True, 0)

    def draw(self):
        if game_manager.in_pause:
            screen.blit(storage.fade_image, storage.fade_image.get_rect())
            print_text("PAUSE", storage.font50, WHITE, 550, 170)
        screen.blit(self.image, self.rect)
        self.start_button.draw()
        self.exit_button.draw()
        screen.blit(self.joystick_image,self.joystick_rect)

    def start_or_pause(self):
        if not game_manager.in_game:
            game_manager.in_game = True
            game_manager.in_pause = False
        else:
            game_manager.in_game = False
            game_manager.in_pause = True

    def exit(self):
        sys.exit()


# Класс кнопки
class Button:
    def __init__(self, images, x, y, func):
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.on = False
        self.func = func
        self.last_update = pygame.time.get_ticks()

    def update(self):
        if self.on:
            now = pygame.time.get_ticks()
            self.image = self.images[1]
            if now - self.last_update > 1000:
                self.on = False
                self.last_update = now
        else:
            self.image = self.images[0]

    def click(self):
        if mouse_in_rect(self.rect):
            self.on = True
            self.func()

    def draw(self):
        screen.blit(self.image, self.rect)

# Класс хранилища всех ресурсов игры
class Storage:
    def __init__(self):
        self.gamebox_images = load_images("background", 7, 1200, 700)
        self.joystick_images = load_images("joystick", 5, 191, 167)
        self.taxi_images = load_images("taxi", 6, 100, 200)
        self.road_images = load_images("road", 2, 1200, 400)
        self.cars_images = []
        for color in ["blue", "green", "lightblue", "red"]:
            self.cars_images.append(load_images(f"car_{color}", 6, 100, 200))
        self.humans_images = []
        for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
            self.humans_images.append(load_images(f"human_v{i}_", 7, 90, 90))
        self.buttonblue_images = load_images("buttonblue", 2, 170, 92)
        self.buttonred_images = load_images("buttonred", 2, 170, 92)
        self.fade_image = load_image("fade", WIDTH, HEIGHT)
        self.fade_image.set_alpha(100)
        font_path = resource_path(os.path.join("venv\\Sprites\\", "TaxiDriver.ttf"))
        self.font10 = pygame.font.Font(font_path, 10)
        self.font16 = pygame.font.Font(font_path, 16)
        self.font25 = pygame.font.Font(font_path, 25)
        self.font50 = pygame.font.Font(font_path, 50)


# Класс контроллера игры(поведение во время игры и паузы)
class GameManager:
    def __init__(self):
        self.in_game = True
        self.in_pause = False
        self.game_speed = 2 + score_board.scores / 10

    def click(self):
        print(pygame.mouse.get_pos())

    def update(self):
        self.game_speed = 2 + score_board.scores / 10
        if self.in_game and not self.in_pause:
            gamebox.update()
            player.update()
            traffic.update()
            humans.update()
            all_cars.update()
            all_humans.update()
            all_roads.update()
        if self.in_pause and not self.in_game:
            pass

    def draw(self):
        if self.in_game and not self.in_pause:
            all_roads.draw(screen)
            all_cars.draw(screen)
            all_humans.draw(screen)
            player.draw()
            score_board.draw()
            gamebox.draw()
        if self.in_pause and not self.in_game:
            all_roads.draw(screen)
            all_cars.draw(screen)
            all_humans.draw(screen)
            player.draw()
            score_board.draw()
            gamebox.draw()


# функция анимации (смена изображения сущности через каждое определенное время)
def animation(Entity, images, speed, endless, angle=0):
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
            if angle == 0:
                Entity.image = images[Entity.i]
            else:
                Entity.image = pygame.transform.rotate(images[Entity.i], angle)
            return is_alive


# функция, которая возвращает булевый ответ, находится ли мышь на обьекте
def mouse_in_rect(rect):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    return rect.left < mouse_x < rect.left + rect.width and rect.top < mouse_y < rect.top + rect.height


# функция загрузки одного изображения
def load_image(name, scaleX, scaleY):
    try:
        return pygame.transform.scale(
            pygame.image.load(resource_path(os.path.join("venv\\Sprites\\", str(name) + ".png"))).convert_alpha(),
            (scaleX, scaleY))
    except Warning:
        print(Warning)


# функция отображения текста на экране
def print_text(text, font, color, x, y):
    surface = font.render(text, True, color)
    screen.blit(surface, pygame.Rect((x, y), (surface.get_rect().width, surface.get_rect().height)))


# функция загрузки нескольких изображений
def load_images(name, count, scaleX, scaleY):
    array = []
    for i in range(count):
        array.append(load_image(str(name) + str(i + 1), scaleX, scaleY))
    return array


# создание сущностей классов и групп для их содержания
storage = Storage()
# bg = pygame.transform.scale(storage.cars_images[0][1], (2000,2000))
all_cars = pygame.sprite.Group()
all_roads = pygame.sprite.Group()
all_humans = pygame.sprite.Group()
score_board = ScoreBoard()
game_manager = GameManager()
for road in [Road(y=-400, type=0), Road(y=0, type=0), Road(y=400, type=1)]:
    all_roads.add(road)
all_humans = pygame.sprite.Group()
# menu = Menu()
gamebox = GameBox()
player = Player()
traffic = Traffic()
humans = Humans()

# сам цикл игры (отслеживание нажатий, обновление и отображение всех сущностей каждый тик)
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_manager.in_game = not game_manager.in_game
                game_manager.in_pause = not game_manager.in_pause
        if event.type == pygame.constants.MOUSEBUTTONDOWN:
            game_manager.click()
            gamebox.start_button.click()
            gamebox.exit_button.click()
    game_manager.update()
    game_manager.draw()
    pygame.display.flip()
sys.exit()
