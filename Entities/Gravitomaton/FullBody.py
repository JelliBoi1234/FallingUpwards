import pygame


class FullGravitomaton(pygame.sprite.Sprite):
    def __init__(self, v, startPos):
        super(FullGravitomaton, self).__init__()

        self.v = v

        self.surf = pygame.image.load(f"{self.v.path}\\Textures\\fullGravitomaton.png").convert()
        self.surf = pygame.transform.scale(self.surf, [70, 70])
        self.surf.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        self.rect = self.surf.get_rect()

        self.rect.move(startPos[0], startPos[1])
        self.v.windo.blit(self.surf, self.rect)

        self.momentum = [0, 0]

    def update(self):

        x = self.rect.x + self.momentum[0]
        y = self.rect.y + self.momentum[1]

        if x < 0:
            x = 0
        if x > self.v.SCREEN_WIDTH:
            x = self.v.SCREEN_WIDTH
        if y < 0:
            y = 0
        if y > self.v.SCREEN_HEIGHT:
            y = self.v.SCREEN_HEIGHT

        self.rect.move(x, y)

    def show(self):
        self.v.windo.blit(self.surf, self.rect)



