import pygame as pg

FPS = 60
WIDTH, HEIGHT = 1408, 896

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Игра")
pg.display.set_icon(pg.image.load("icon.png"))
clock = pg.time.Clock()


class Player:
    COLOR = (0, 0, 255)
    WIDTH, HEIGHT = 100, 100
    SPEED = 3

    def __init__(self):
        self.surf = pg.Surface((Player.WIDTH, Player.HEIGHT), pg.SRCALPHA)
        self.rect = self.surf.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.speed = 3
        self.mask = pg.mask.from_surface(self.surf)
        self.surf.fill((0, 0, 0, 0))
        pg.draw.circle(self.surf, (*Player.COLOR, 255),
                       (self.rect.width / 2, self.rect.height / 2), 30)

    def move(self, dx=0, dy=0):
        if (self.rect.left + dx * self.speed) > 0 and (self.rect.right + dx * self.speed) < WIDTH:
            self.rect.x += dx * self.speed
        if (self.rect.top + dy * self.speed) > 0 and (self.rect.bottom + dy * self.speed) < HEIGHT:
            self.rect.y += dy * self.speed

    def draw(self, screen):
        screen.blit(self.surf, self.rect)


class Potato:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.thirst = False
        self.surf = pg.image.load("Images/Potato/Potato_first.png").convert_alpha()
        self.surf_icon = pg.image.load("Images/Icons/Thirst_icon_full.png").convert_alpha()
        self.rect = self.surf.get_rect(center=(self.x, self.y))
        self.rect_icon = self.rect
        self.stage = 1
        self.iter_counter = 0

    def draw(self, screen):
        screen.blit(self.surf, self.rect)
        screen.blit(self.surf_icon, self.rect_icon)

    def grow(self):
        if self.thirst:
            if self.iter_counter > 460:
                if self.stage == 1:
                    self.surf = pg.image.load("Images/Potato/Potato_second.png")
                    self.drying_out()
                if self.stage == 2:
                    self.surf = pg.image.load("Images/Potato/Potato_third.png")
                    self.drying_out()
                if self.stage == 3:
                    self.surf = pg.image.load("Images//Potato/Potato_premax.png")
                    self.drying_out()
                if self.stage == 4:
                    self.surf = pg.image.load("Images//Potato/Potato_max.png")
                self.rect = self.surf.get_rect(center=(self.x, self.y))
                self.stage += 1
                self.iter_counter = 0
            self.iter_counter += 1

    def irrigation(self):
        self.thirst = True
        self.surf_icon.fill((0, 0, 0, 0))

    def drying_out(self):
        self.thirst = False
        self.surf_icon = pg.image.load("Images/Icons/Thirst_icon_full.png").convert_alpha()


class Wheat:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.thirst = False
        self.surf = pg.image.load("Images//Wheat/Wheat_first.png").convert_alpha()
        self.surf_icon = pg.image.load("Images/Icons/Thirst_icon_full.png").convert_alpha()
        self.rect = self.surf.get_rect(center=(self.x, self.y))
        self.rect_icon = self.rect
        self.stage = 1
        self.iter_counter = 0

    def draw(self, screen):
        screen.blit(self.surf, self.rect)
        if not self.thirst:
            screen.blit(self.surf_icon, self.rect_icon)

    def grow(self):
        if self.iter_counter > 960:
            if self.stage == 1 and self.thirst:
                self.surf = pg.image.load("Images/Wheat/Wheat_second.png")
                self.drying_out()
            if self.stage == 2 and self.thirst:
                self.surf = pg.image.load("Images/Wheat/Wheat_third.png")
                self.drying_out()
            if self.stage == 3 and self.thirst:
                self.surf = pg.image.load("Images//Wheat/Wheat_premax.png")
                self.drying_out()
            if self.stage == 4 and self.thirst:
                self.surf = pg.image.load("Images//Wheat/Wheat_max.png")
            self.rect = self.surf.get_rect(center=(self.x, self.y))
            self.stage += 1
            self.iter_counter = 0
        self.iter_counter += 1

    def irrigation(self):
        self.thirst = True
        self.surf_icon.fill((0, 0, 0, 0))

    def drying_out(self):
        self.thirst = False
        self.surf_icon = pg.image.load("Images/Icons/Thirst_icon_full.png").convert_alpha()


def check_collusions(player, plants):
    inds = player.rect.collidelistall([elem.rect for elem in plants])
    for i in inds:
        plants[i].irrigation()


background_surf = pg.image.load("Images/background_standardmaps.png").convert_alpha()
wheat = []
cords = []
potatoes = []
iters = 0
player = Player()
pg.display.update()
screen.blit(background_surf, (0, 0))

flag_play = True
while flag_play:
    clock.tick(FPS)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            flag_play = False
            break
    if not flag_play:
        break

    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT]:
        player.move(dx=-1)
    if keys[pg.K_RIGHT]:
        player.move(dx=1)
    if keys[pg.K_UP]:
        player.move(dy=-1)
    if keys[pg.K_DOWN]:
        player.move(dy=1)
    if keys[pg.K_e] and iters > 60:
        potatoes.append(Potato(player.rect.centerx, player.rect.centery))
        iters = 0
    if keys[pg.K_q] and iters > 60:
        for i in range(11):
            if i == player.rect.centerx // 128:
                print(i + 1, end=" ")
                x = i * 128 + 64
                break
        for i in range(7 + 1):
            if i == player.rect.centery // 128:
                print(i + 1)
                y = i * 128 + 64
                break
        print(x, y)
        wheat.append(Wheat(x, y))
        iters = 0
    if keys[pg.K_SPACE] and iters > 60:
        iters = 0
        check_collusions(player, potatoes)
        check_collusions(player, wheat)

    screen.blit(background_surf, (0, 0))
    for elem in potatoes:
        elem.draw(screen)
        elem.grow()
    for elem in wheat:
        elem.draw(screen)
        elem.grow()
    player.draw(screen)
    pg.display.update()
    iters += 1