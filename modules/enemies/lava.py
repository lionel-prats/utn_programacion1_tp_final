import pygame 
from modules.enemies.enemy import Enemy

class Lava(Enemy):
    def __init__(self, image, x, y, tile_size):
        Enemy.__init__(self, image, x, y)
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size // 2))
        
        # pongo a la lava sobre el suelo si su altura es menor a la de las baldosas
        if self.rect.height < tile_size:
            self.rect.y += abs(self.rect.height - tile_size) 
     
        self.counter = 0

    def update(self):
        self.counter += 1
        if self.counter > 15:
            self.image = pygame.transform.flip(self.image, True, False)
            self.counter = 0