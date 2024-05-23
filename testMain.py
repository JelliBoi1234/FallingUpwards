import pygame, pathlib
from Assets.gameLoop import *
from Assets.Vars import *
from Entities.Gravitomaton.FullBody import *


def run(e):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            v.gameLoop.stop()
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                v.gameLoop.stop()

    v.windo.fill((255, 255, 255))

    for e in v.entities:
        e.run()

    pygame.display.flip()


pygame.init()

v = Vars()
v.path = str(pathlib.Path(__file__).parent)
v.FPS = 30
v.SCREEN_WIDTH = 800
v.SCREEN_HEIGHT = 800
v.windo = pygame.display.set_mode([v.SCREEN_WIDTH, v.SCREEN_HEIGHT])
v.gameLoop = Loop(v, run)
v.entities = pygame.sprite.Group()
v.player = FullGravitomaton(v, [v.SCREEN_WIDTH/2, v.SCREEN_HEIGHT])
v.entities.add(v.player)

# v.gameLoop.addProcess("Update Movement", v.player.updateKeys, None)
# v.gameLoop.addProcess("Update Gravity", v.player.gravityUpdate, None)
# v.gameLoop.addProcess("update Pos", v.player.updatePos, None)
v.gameLoop.run()
