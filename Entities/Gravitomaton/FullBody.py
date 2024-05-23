import pygame
import numpy as np


class FullGravitomaton(pygame.sprite.Sprite):
    def __init__(self, v, startPos):
        super(FullGravitomaton, self).__init__()

        self.v = v

        self.surf = pygame.image.load(f"{self.v.path}\\Textures\\fullGravitomaton.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, [70, 70])
        self.rect = self.surf.get_rect()
        self.rotation = 0  # degrees

        print(self.rect.midtop, self.rect.midleft, self.rect.midright, self.rect.midbottom)

        self.rect.move_ip(startPos[0] - self.rect.width/2, startPos[1] - self.rect.height)
        self.show()

        self.momentum = [0, 0]
        self.momentumFactor = [10, -20]

        self.direction = "bottom"
        self.directions = {}
        self._refreshDirections()

        self.multipliers = {"bottom": [1, 1],
                           "top": [-1, -1],
                           "left": [-1, 1],
                           "right": [1, -1]}

        self.force = [0, 0]

        self.collided = False
        self.anchored = False
        self.fall = True

        self.jumping = False
        self.maxJumps = 2
        self.jumps = 0

        self.moving = False
        self.friction = 2
        self.gravity = 1

    def updatePos(self):
        self._refreshDirections()
        self.collided = False

        self.force[0] += self.directions[self.direction][0]
        self.force[1] += self.directions[self.direction][1]

        x, y = self.force

        if self.rect.x + x < 0:
            self.rect.move(0, self.rect.y)
            self.force[0] = 0
            self.collided = True

            if self.direction == "left":
                self.jumping = False
                self.jumps = 0

        if self.rect.x + x > self.v.SCREEN_WIDTH - self.rect.width:
            self.rect.move(self.v.SCREEN_WIDTH - self.rect.width, self.rect.y)
            self.force[0] = 0
            self.collided = True

            if self.direction == "right":
                self.jumping = False
                self.jumps = 0

        if self.rect.y + y < 0:
            self.rect.move(self.rect.x, 0)
            self.force[1] = 0
            self.collided = True

            if self.direction == "top":
                self.jumping = False
                self.jumps = 0

        if self.rect.y + y > self.v.SCREEN_HEIGHT - self.rect.height:
            self.rect.move(self.rect.x, self.v.SCREEN_HEIGHT - self.rect.height)
            self.force[1] = 0
            self.collided = True

            if self.direction == "bottom":
                self.jumping = False
                self.jumps = 0

        # print(self.force, (self.rect.x, self.rect.y), self.collided, self.anchored)

        self.rect.move_ip(self.force[0], self.force[1])

    def basicMovement(self, key):
        self.momentum = [0, 0]

        if not key[pygame.K_SPACE] and not key[pygame.K_w] and self.jumping and self.jumps < self.maxJumps:
            self.jumping = False

        if (key[pygame.K_w] or key[pygame.K_SPACE]) and not self.jumping:
            self.momentum[1] += self.momentumFactor[1]
            self.jumping = True
            self.jumps += 1

        if key[pygame.K_a] and not self.jumping and not self.moving:
            self.momentum[0] = -self.momentumFactor[0]
            self.moving = True
        elif key[pygame.K_d] and not self.jumping and not self.moving:
            self.momentum[0] = self.momentumFactor[0]
            self.moving = True
        else:
            self.moving = False

        if (key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT] or key[pygame.K_s]) and (self.collided or self.anchored):
            self.force = [0, 0]
            self.momentum = [0, 0]
            self.anchored = True
            self.fall = False
            self.jumping = False
            self.jumps = 0
        else:
            self.fall = True
            self.anchored = False

        self._refreshDirections()

    def directionUpdate(self, key):

        if key[pygame.K_DOWN]:
            self.direction = "bottom"
            self.rotate(0)
            print(self.direction)
        elif key[pygame.K_UP]:
            self.direction = "top"
            self.rotate(180)
            print(self.direction)
        elif key[pygame.K_LEFT]:
            self.direction = "left"
            self.rotate(270)
            print(self.direction)
        elif key[pygame.K_RIGHT]:
            self.direction = "right"
            self.rotate(90)
            print(self.direction)

    def gravityUpdate(self):

        if self.force[0] == 0:
            pass
        elif not self.jumping and self.force[0] != 0 and self.direction == "bottom":
            self.momentum[0] -= self.force[0]/self.friction
        elif not self.jumping and self.force[0] != 0 and self.direction == "top":
            self.momentum[0] += self.force[0]/self.friction

        if self.force[1] == 0:
            pass
        elif not self.jumping and self.force[1] != 0 and self.direction == "right":
            self.momentum[0] += self.force[1]/self.friction
        elif not self.jumping and self.force[1] != 0 and self.direction == "left":
            self.momentum[0] -= self.force[1]/self.friction

        if self.fall and not self.collided and not self.anchored:
            self.momentum[1] += self.gravity

        self._refreshDirections()

    def run(self):
        key = pygame.key.get_pressed()

        self.basicMovement(key)

        self.directionUpdate(key)

        self.gravityUpdate()

        self.updatePos()

        self.show()

    def _refreshDirections(self):
        self.directions = {"bottom": [self.momentum[0], self.momentum[1]],
                           "top": [-self.momentum[0], -self.momentum[1]],
                           "left": [-self.momentum[1], self.momentum[0]],
                           "right": [self.momentum[1], -self.momentum[0]]}

    def rotate(self, a):
        self.surf = pygame.transform.rotate(self.surf, a - self.rotation)
        self.rotation = a

    def show(self):
        self.v.windo.blit(self.surf, self.rect)
