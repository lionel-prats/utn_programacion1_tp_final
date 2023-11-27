import pygame

class Exit(pygame.sprite.Sprite):
    def __init__(self, path_img, x, y, tile_size):
        pygame.sprite.Sprite.__init__(self)
        
        img = pygame.image.load(path_img)
        
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        
        self.rect = self.image.get_rect()
        
        self.rect.x = x

        self.rect.y = y - tile_size // 2        