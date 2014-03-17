import pygame
from pygame.locals import *

# Utility methods
import random

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

def load_sliced_sprites(w, h, rows, filename):
    '''
    Specs :
        Master can be any height.
        Sprites frames width must be the same width
        Master width must be len(frames)*frame.width
    Assuming you ressources directory is named "ressources"
    '''
    images = []
    master_image = pygame.image.load(filename)

    master_width, master_height = master_image.get_size()
    for row in xrange(rows):
        for i in xrange(int(master_width/w)):
            images.append(master_image.subsurface((i*w,row*h,w,h)))

    return images

class Bird(pygame.sprite.Sprite):

    """
    Our flappy bird
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self._images = []
        self._images.append(pygame.image.load('plane_1.png'))
        self._images.append(pygame.image.load('plane_2.png'))

        self.image = self._images[0]

        self.rect = self.image.get_rect()

        self.rect.x = SCREEN_WIDTH / 2 - 20
        self.rect.y = SCREEN_HEIGHT / 2

        self._space_pressed = False

        self._delay = 1000/30 # change to global
        self._last_update = 0
        self._frame = 0


    def update(self, t):
        if t - self._last_update > self._delay:
            self._frame += 1
            if self._frame >= len(self._images): self._frame = 0
            self.image = self._images[self._frame]
            self._last_update = t

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

        self.image = pygame.image.load('coin.png')

        self.rect = self.image.get_rect()

        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.random() * SCREEN_HEIGHT

        self.x_velocity = -10

    def update(self):
        self.rect.x += self.x_velocity

class GameOver(pygame.sprite.Sprite):

    '''GameOver class'''

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('GameOver.jpeg')

        self.rect = self.image.get_rect()

        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.random() * SCREEN_HEIGHT

        self.x_velocity = -10

    #def update(self)
   

class Explode(pygame.sprite.Sprite):

    '''Explode class'''

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self._images = load_sliced_sprites(48, 48, 2, 'explosions.png')

        self.image = pygame.image.load('Explode.png')
        self.rect = self.image.get_rect()

        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.random() * SCREEN_HEIGHT
        self._exploding = False

        self.x_velocity = -10
        self._delay = 1000/30 # change to global
        self._last_update = 0
        self._frame = 0

    def update(self, t):
        if self._exploding and t - self._last_update > self._delay:
            self._frame += 1
            if self._frame >= len(self._images): self._frame = len(self._images) - 1
            self.image = self._images[self._frame]
            self._last_update = t

        if not self._exploding:
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
        self._explode_group = pygame.sprite.Group()
        self._gameover_group = pygame.sprite.Group()

        # Whether bird is alive

        self._alive = True

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
        self._bird_group.update(pygame.time.get_ticks())
        if random.randrange(1, 11) == 1:
            coin = Coin()
            gameover = GameOver()
            self._coin_group.add(coin)

        if random.randrange(1, 11) == 1:    
            explode = Explode()
            self._explode_group.add(explode)
        
        self._explode_group.update(pygame.time.get_ticks())

        if self._alive:
            self._coin_group.update()

            for coin in self._coin_group.sprites():
                if coin.rect.colliderect(self._bird.rect):
                    self._coin_group.remove(coin)
                if coin.rect.x < 0 - coin.rect.width:
                    self._coin_group.remove(coin)

            for explode in self._explode_group.sprites():
                if explode.rect.colliderect(self._bird.rect):
                    self._alive = False
                    explode._exploding = True
                if explode.rect.x < 0 - explode.rect.width:
                    self._explode_group.remove(explode)        


    def on_render(self):
        self._display_surf.fill([255, 255, 255])
        if self._alive:
            self._bird_group.draw(self._display_surf)
        else:
            # Draw explosion where the bird is
            pass
        self._coin_group.draw(self._display_surf)
        self._explode_group.draw(self._display_surf)
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
