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

        self.rect = self.rect.move(startPos[0], startPos[1])
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

        if self.rect.left + x < 0 and self.rect.left <= 0:
            self.rect.left = -1
            self.force[0] = 0
            self.collided = True

            if self.direction == "left":
                self.jumping = False
                self.jumps = 0
                self.force[0] = 0

        if self.rect.right + x > self.v.SCREEN_WIDTH and self.rect.right >= self.v.SCREEN_WIDTH:
            self.rect.right = self.v.SCREEN_WIDTH + 1
            self.force[0] = 0
            self.collided = True

            if self.direction == "right":
                self.jumping = False
                self.jumps = 0
                self.force[0] = 0

        if self.rect.top + y < 0 and self.rect.top <= 0:
            self.rect.top = -1
            self.force[1] = 0
            self.collided = True

            if self.direction == "top":
                self.jumping = False
                self.jumps = 0
                self.force[1] = 0

        if self.rect.bottom + y > self.v.SCREEN_HEIGHT and self.rect.bottom >= self.v.SCREEN_HEIGHT:
            self.rect.bottom = self.v.SCREEN_HEIGHT + 1
            self.force[1] = 0
            self.collided = True

            if self.direction == "bottom":
                self.jumping = False
                self.jumps = 0
                self.force[1] = 0

        print(f"Force: {self.force}, momentum: {self.momentum}, Pos: {self.rect.x, self.rect.y}, IsCollided: {self.collided}, IsAnchored: {self.anchored}")

        self.rect.move_ip(self.force[0], self.force[1])

    def basicMovement(self, key):
        self.momentum = [0, 0]

        if not key[pygame.K_SPACE] and not key[pygame.K_w] and self.jumping and self.jumps <= self.maxJumps:
            self.jumping = False

        if (key[pygame.K_w] or key[pygame.K_SPACE]) and not self.jumping and self.jumps < self.maxJumps and not self.anchored:
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

        if (key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT] or key[pygame.K_s]) and self.collided and not self.jumping:
            self.force = [0, 0]
            self.momentum = [0, 0]
            self.anchored = True
            self.jumping = False
            self.jumps = 0
        else:
            self.anchored = False

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

        # makes the player slow down when moving (for top and bottom sides, only enacting when the player is moving)
        if self.force[0] == 0:
            pass
        elif not self.jumping and self.force[0] != 0 and self.direction == "bottom":
            self.momentum[0] -= self.force[0]/self.friction
        elif not self.jumping and self.force[0] != 0 and self.direction == "top":
            self.momentum[0] += self.force[0]/self.friction

        # makes the player slow down when moving (for right and left sides, only enacting when the player is moving)
        if self.force[1] == 0:
            pass
        elif not self.jumping and self.force[1] != 0 and self.direction == "right":
            self.momentum[0] += self.force[1]/self.friction
        elif not self.jumping and self.force[1] != 0 and self.direction == "left":
            self.momentum[0] -= self.force[1]/self.friction

        # makes player fall (momentum is based on what side the player is on)
        if self.fall and not self.anchored:
            self.momentum[1] += self.gravity

    def run(self):
        key = pygame.key.get_pressed()

        self.basicMovement(key)

        self.directionUpdate(key)

        self.gravityUpdate()

        self._refreshDirections()

        self.updatePos()

        self.recenter(key)

        self.show()

    def _refreshDirections(self):
        self.directions = {"bottom": [self.momentum[0], self.momentum[1]],
                           "top": [-self.momentum[0], -self.momentum[1]],
                           "left": [-self.momentum[1], self.momentum[0]],
                           "right": [self.momentum[1], -self.momentum[0]]}

    def recenter(self, keys):
        if keys[pygame.K_r]:
            self.force = [0, 0]
            self.momentum = [0, 0]
            self.rect = self.rect.move(self.v.SCREEN_WIDTH/2, self.v.SCREEN_HEIGHT/2)

    def rotate(self, a):
        self.surf = pygame.transform.rotate(self.surf, a - self.rotation)
        self.rotation = a

    def show(self):
        self.v.windo.blit(self.surf, self.rect)
