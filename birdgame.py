import pygame
from pygame.locals import *

# Utility methods
import random

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480


class Bird(pygame.sprite.Sprite):

    """
    Our flappy bird
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('plane_1.png')

        self.rect = self.image.get_rect()

        self.rect.x = SCREEN_WIDTH / 2 - 20
        self.rect.y = SCREEN_HEIGHT / 2

        self._space_pressed = False

    def update(self):
        if self._space_pressed:
            self.y_velocity = -10
        else:
            self.y_velocity = 10
        self.rect.y += self.y_velocity

        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > SCREEN_HEIGHT - self.rect.height:
            self.rect.y = SCREEN_HEIGHT - self.rect.height


class Coin(pygame.sprite.Sprite):

    '''Coin class'''

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('coin.jpeg')

        self.rect = self.image.get_rect()

        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.random() * SCREEN_HEIGHT

        self.x_velocity = -10

    def update(self):
        self.rect.x += self.x_velocity


class App:

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._clock = pygame.time.Clock()

        self._bird_group = pygame.sprite.Group()
        self._bird = Bird()
        self._bird_group.add(self._bird)

        self._coin_group = pygame.sprite.Group()

        self._fps = 30

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        return True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == KEYUP:
            if event.key == pygame.K_SPACE:
                self._bird._space_pressed = False

        elif event.type == KEYDOWN:
            if event.key == pygame.K_SPACE:
                self._bird._space_pressed = True

    def on_loop(self):
        self._bird_group.update()
        if random.randrange(1, 11) == 1:
            coin = Coin()
            self._coin_group.add(coin)

        self._coin_group.update()

        for coin in self._coin_group.sprites():
            if coin.rect.colliderect(self._bird.rect):
                self._coin_group.remove(coin)
            if coin.rect.x < 0 - coin.rect.width:
                self._coin_group.remove(coin)

    def on_render(self):
        self._display_surf.fill([255, 255, 255])
        self._bird_group.draw(self._display_surf)
        self._coin_group.draw(self._display_surf)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if not self.on_init():
            self._running = False

        while(self._running):
            self._clock.tick(self._fps)
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
