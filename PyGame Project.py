import pygame as pg

FPS = 60
WIDTH, HEIGHT = 1000, 600

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Игра")
pg.display.set_icon(pg.image.load(r"icon.png"))
clock = pg.time.Clock()


class Player:
    COLOR = (0, 0, 255)
    WIDTH, HEIGHT = 100, 100
    SPEED = 3

    def __init__(self):
        self.surf = pg.Surface((Player.WIDTH, Player.HEIGHT), pg.SRCALPHA)
        self.rect = self.surf.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.speed = 3
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
        self.surf = pg.image.load("images/Growth_first.png").convert_alpha()
        self.rect = self.surf.get_rect(center=(self.x, self.y))
        self.stage = 1
        self.iter_counter = 0

    def draw(self, screen):
        screen.blit(self.surf, self.rect)

    def grow(self):
        if self.iter_counter > 360:
            if self.stage == 1:
                self.surf = pg.image.load("images/Growth_second.png")
            if self.stage == 2:
                self.surf = pg.image.load("images/Growth_third.png")
            if self.stage == 3:
                self.surf = pg.image.load("images/Growth_premax.png")
            if self.stage == 4:
                self.surf = pg.image.load("images/Growth_max.png")
            self.rect = self.surf.get_rect(center=(self.x, self.y))
            self.stage += 1
            self.iter_counter = 0

        self.iter_counter += 1



potatoes = []
iters = 0
player = Player()
pg.display.update()

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
    if keys[pg.K_SPACE] and iters > 60:
        potatoes.append(Potato(player.rect.centerx, player.rect.centery))
        iters = 0


    screen.fill((255, 255, 255))
    for elem in potatoes:
        elem.draw(screen)
        elem.grow()
    player.draw(screen)
    pg.display.update()
    iters += 1