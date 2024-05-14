import pygame, pathlib
from Assets.gameLoop import *
from Assets.Vars import *
from Entities.Gravitomaton.FullBody import *


def run(e):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            v.gameLoop.stop()

    v.windo.fill((0, 0, 0))

    for e in v.entities:
        e.show()

    pygame.display.flip()


pygame.init()

v = Vars()
v.path = str(pathlib.Path(__file__).parent)
v.FPS = 100
v.SCREEN_WIDTH = 600
v.SCREEN_HEIGHT = 600
v.windo = pygame.display.set_mode([v.SCREEN_WIDTH, v.SCREEN_HEIGHT])
v.gameLoop = Loop(v, run)
v.entities = pygame.sprite.Group()
v.player = FullGravitomaton(v, [300, 300])
v.entities.add(v.player)

v.gameLoop.addProcess("update", v.player.update, None)
v.gameLoop.run()

