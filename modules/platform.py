import pygame 

class Platform(pygame.sprite.Sprite):
    def __init__(self, path_image, x, y, tile_size, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(path_image)
        self.image = pygame.transform.scale(img, (tile_size, tile_size//2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_counter = 0
        self.move_direction = 1
        self.move_x = move_x
        self.move_y = move_y

    def update(self):
        
        self.rect.x += self.move_direction * self.move_x # si self.move_x == 1 se movera sobre el eje X, si 0 no lo hara 
        self.rect.y += self.move_direction * self.move_y # si self.move_y == 1 se movera sobre el eje Y, si 0 no lo hara
        self.move_counter += 1 

        if abs(self.move_counter) > 50: # infinite loop -> 50f to right, 100f to left, 100f to right, 100f to left...
            self.move_direction *= -1
            self.move_counter *= -1